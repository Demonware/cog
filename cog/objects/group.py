# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms

# user group object handling

import os
import sys
from functools import wraps

import ldap
import ldap.modlist as modlist

import cog.directory as dir
import cog.util as util
from cog.config import Profiles

settings = Profiles().current()

rfc2307bis = False
rfc2307bis_object_class = settings.get('rfc2307bis_group_object_class')
rfc2307bis_member_attribute = settings.get('rfc2307bis_group_member_attribute')
rfc2307bis_sync = settings.get('rfc2307bis_group_sync_attributes')

if dir.is_auxiliary('posixGroup') and dir.is_structural(rfc2307bis_object_class):
    rfc2307bis = True


class Group(object):
    def __init__(self, gid, group_data=None):
        self.tree = dir.Tree()
        self.gid = gid
        self.base_dn = settings.get('group_dn')
        self.ldap_query = settings.get('group_query') % (self.gid)
        self.exists = True
        groups = self.tree.search(self.base_dn, search_filter=self.ldap_query)
        if len(groups) > 1:
            raise dir.MultipleObjectsFound
        elif len(groups) == 1:
            self.data = groups[0]
        else:
            self.exists = False
            self.data = group_data
            if rfc2307bis:
                self.data.append('objectClass', rfc2307bis_object_class)

    def group_exists(method):
        """
        Make sure that you're operating on an existing object."
        """
        @wraps(method)
        def _group_exists(self, *args, **kwargs):
            if not self.exists:
                raise dir.ObjectNotFound("Group ‘%s’ cannot be found." % self.cn)
            return method(self, *args, **kwargs)
        return _group_exists

    def add(self):
        self.tree.add(self.data)
        self.exists = True

    @group_exists
    def set_description(self, description):
        self.data.replace('description', description)
        self.tree.modify(self.data)

    @group_exists
    def rename(self, new_gid):
        self.tree.rename(self.dn, new_gid)

    @group_exists
    def remove(self):
        self.tree.remove(self.data.dn)

    @group_exists
    def add_uid(self, uids):
        if type(uids) is not list:
            uids = [uids]
        for uid in uids:
            if ('memberUid' not in self.data or
                  uid not in self.data['memberUid']):
                self.data.append('memberUid', uid)
            if rfc2307bis:
                uid_dn = dir.find_dn_for_uid(uid)
                if not uid_dn:
                    raise dir.ObjectNotFound("User object not found.")
                if (rfc2307bis_member_attribute not in self.data or
                      uid_dn not in self.data[rfc2307bis_member_attribute]):
                    self.data.append(rfc2307bis_member_attribute, uid_dn)

    @group_exists
    def del_uid(self, uids):
        if type(uids) is not list:
            uids = [uids]
        for uid in uids:
            self.data.remove('memberUid', uid)
            if rfc2307bis:
                uid_dn = dir.find_dn_for_uid(uid)
                if not uid_dn:
                    raise dir.ObjectNotFound("User object not found.")
                self.data.remove(rfc2307bis_member_attribute, uid_dn)

    @group_exists
    def commit_changes(self):
        self.tree.modify(self.data)

