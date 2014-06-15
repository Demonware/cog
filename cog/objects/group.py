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
        self.tree.modify(self.data.dn, self.data)

    @group_exists
    def rename(self, new_gid):
        self.tree.rename(self.dn, new_gid)

    @group_exists
    def remove(self):
        self.tree.remove(self.data.dn)

    @group_exists
    def add_uid(self, uid):
        if not self.data.has_key('memberUid') or uid not in self.data['memberUid']:
            self.data.append('memberUid', uid)

    @group_exists
    def del_uid(self, uid):
        self.data.remove('memberUid', uid)

    @group_exists
    def commit_changes(self):
        self.tree.modify(self.data.dn, self.data)

