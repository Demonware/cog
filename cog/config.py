# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms

# process configuration files

import os, sys
import yaml
import cog.util as util

user_settings_dir = os.environ['HOME'] + os.sep + '.cog'
sys_settings_dir = '/etc/cog'

def read_yaml(file):
    data = dict()
    try:
        fh = open(file)
        data = yaml.safe_load(fh)
        fh.close()
    except (IOError, yaml.YAMLError), e:
        print e
    return data

def merge_data(*files):
    data = dict()
    for file in files:
        if os.path.exists(file):
            data = util.merge(data, read_yaml(file))
    return data

def expand_inheritances(template_data, section):
    template = dict()
    for k, v in template_data.get(section).iteritems():
        if v.has_key('inherits'):
            base = v.get('inherits')
            template[k] = util.merge(template_data.get(section).get(base).get('default'), v.get('default'))
        else:
            template[k] = v.get('default')
    return template

class Profiles(dict):
    __metaclass__ = util.Singleton

    def __init__(self):

        super(self.__class__, self).__init__({})

        self.defaults = {
            'ldap_uri': 'ldap://ldap/',
            'ldap_encryption': True,
            'bind_dn': None,
            'bind_pass': None,
            'user_rdn': 'uid',
            'user_query': '(&(%s=%s)(|(objectClass=posixAccount)(objectClass=inetOrgPerson)))',
            'group_query': '(&(cn=%s)(objectClass=posixGroup))',
            'netgroup_query': '(&(cn=%s)(objectClass=nisNetgroup))',
            'min_uidnumber': 0,
            'max_uidnumber': 9998,
            'min_gidnumber': 9200,
            'max_gidnumber': 9998
        }

        user_settings_file = user_settings_dir + os.sep + 'settings'
        sys_settings_file = sys_settings_dir + os.sep + 'settings'
        settings_data = merge_data(sys_settings_file, user_settings_file)

        self.profile = settings_data.pop('profile')

        for k, v in settings_data.iteritems():
            self[k] = v

    def list(self):
        return self.keys()

    def current(self, name=None):
        return util.merge(self.defaults, self.get(name or self.profile))

    def use(self, name):
        if name in self.keys():
            self.profile = name


user_template_file = user_settings_dir + os.sep + 'templates.yaml'
sys_template_file = sys_settings_dir + os.sep + 'templates.yaml'

template_data = merge_data(sys_template_file, user_template_file)

objects = dict()
for object in ['accounts', 'groups', 'netgroups']:
    objects[object] = expand_inheritances(template_data, object)

