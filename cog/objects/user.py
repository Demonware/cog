# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms

# user object handling


import os
import sys
import getpass
from functools import wraps

import ldap
import ldap.modlist as modlist

import cog.directory as dir
import cog.util as util
from cog.objects.group import Group

from cog.config import objects, Profiles
accounts = objects.get('accounts')
settings = Profiles().current()

class User(object):
    def __init__(self, name, account_data=None, groups=None, bind=False):
        """
        User object, unsurprisingly.
        """
        self.tree = dir.Tree()
        self.name = name
        self.exists = True
        self.base_dn = settings.get('user_dn')
        self.ldap_query = settings.get('user_query') % (settings.get('user_rdn'), self.name)
        user_data = self.tree.search(self.base_dn, search_filter=self.ldap_query, bind=bind)
        if len(user_data) > 1:
            raise dir.MultipleObjectsFound("The user ID is not unique.")
        if len(user_data) == 1:
            self.data = user_data[0]
            self.uid = self.data.get('uid')
        else:
            self.exists = False
            self.uid = [name]
            self.data = account_data
            self.groups = groups

    def user_exists(method):
        """
        Make sure that you're operating on an existing object."
        """
        @wraps(method)
        def _user_exists(self, *args, **kwargs):
            if not self.exists:
                raise dir.ObjectNotFound("User ‘%s’ cannot be found." % self.name)
            return method(self, *args, **kwargs)
        return _user_exists

    def add(self):
        self.tree.add(self.data)
        self.exists = True
        if self.groups:
            for group in self.groups:
                try:
                    self.addgroup(group)
                except:
                    print "There was a problem with adding user %s to the group %s." % (self.name, group)

    @user_exists
    def replace_item(self, item, value):
        self.data.replace(item, value)

    @user_exists
    def append_to_item(self, item, value):
        self.data.append(item, value)

    @user_exists
    def remove_from_item(self, item, value):
        self.data.remove(item, value)

    @user_exists
    def commit_changes(self):
        self.tree.modify(self.data.dn, self.data)

    @user_exists
    def find_groups(self):
        for uid in self.uid:
            groups = [x['cn'][0] for x in self.tree.search(search_filter='(&(objectClass=posixGroup)(memberUid=%s))' % uid, attributes=['cn'])]
            yield groups

    @user_exists
    def strip_groups(self):
        for uid in self.uid:
            groups = [x['cn'][0] for x in self.tree.search(search_filter='(&(objectClass=posixGroup)(memberUid=%s))' % uid, attributes=['cn'])]
            for group in groups:
                self.delgroup(group)

    @user_exists
    def addgroup(self, user_group):
        group_obj = Group(user_group)
        for uid in self.uid:
            group_obj.add_uid(uid)
        group_obj.commit_changes()

    @user_exists
    def delgroup(self, user_group):
        group_obj = Group(user_group)
        for uid in self.uid:
            group_obj.del_uid(uid)
        group_obj.commit_changes()

    @user_exists
    def set_password(self, password=None):
        if not password:
            password = getpass.getpass('enter new LDAP password for %s: ' % self.name)
        self.data.replace('userPassword', util.make_pass(password))
        self.tree.modify(self.data.dn, self.data)

    @user_exists
    def rename(self, new_name):
        self.tree.rename(self.data.dn, new_rdn='%s=%s'
                         % (settings.get('user_rdn'), new_name))

    @user_exists
    def remove(self):
        self.strip_groups()
        self.tree.remove(self.data.dn)

    @user_exists
    def retire(self):
        self.set_password(util.randomized_string(32))
        self.data.replace('gidNumber', accounts.get('retired').get('gidNumber'))
        self.tree.modify(self.data.dn, self.data)
        self.tree.move(self.data.dn, new_parent=dir.get_account_base('retired'))
        self.strip_groups()
