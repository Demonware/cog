# -*- coding: utf-8 -*-
#!/usr/bin/python

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms


import sys
import getpass
import argparse
import yaml
import cog.util as util
import cog.directory as dir
from cog.objects.group import Group
from cog.config import objects, Profiles

from group_argparser import tool_parser, arg_no

groups = objects.get('groups')
settings = Profiles().current()

def add_group(args, group_type):
    group_data = util.merge(groups.get(group_type), args)
    if group_type in groups.keys():
        cn = group_data.get('cn')
        path = group_data.pop('path', None)
        requires = group_data.pop('requires', None)
        if not group_data.get('gidNumber') and 'gidNumber' in requires:
            group_data['gidNumber'] = dir.get_probably_unique_gidnumber()
        dn = "cn=%s,%s" % (cn, dir.get_group_base(group_type))
        group_entry = dir.Entry(dn=dn, attrs=group_data)
        newgroup = Group(cn, group_entry)
        newgroup.add()
    else:
        print "group type %s is not exactly known." % group_type
        sys.exit(1)

def edit_group(args):
    group = Group(args.pop('cn'))
    for attr, val in args.iteritems():
        attr = attr.lower()
        if attr == 'description':
            group.set_description(val)
        elif attr == 'addmemberuid':
            group.add_uid(val)
        elif attr == 'delmemberuid':
            group.del_uid(val)
    group.commit_changes()

def rename_group(args):
    group = Group(args.get('cn'))
    group.rename(args.get('newCn'))

def remove_group(cn):
    group = Group(cn)
    group.remove()

def show_group(cn):
    group = Group(cn)
    if group.exists:
        del(group.data['objectClass'])
        data = dict(group.data)
        print yaml.safe_dump({ cn: data }, default_flow_style=False)


def main():
    if arg_no < 2 or sys.argv[1] in ['-h', '--help']:
        print tool_parser.format_help()
        sys.exit(1)

    args = dict((k, v) for k, v in vars(tool_parser.parse_args()).iteritems() if v is not None)
    command = args.pop('command')
    group_type = args.pop('group_type', 'generic')

    if command == 'add':
        add_group(args, group_type)
    elif command == 'edit':
        edit_group(args)
    elif command == 'rename':
        rename_group(args)
    elif command == 'remove':
        remove_group(args.get('cn'))
    elif command == 'show':
        show_group(args.get('cn'))

    sys.exit(0)

if __name__ == "__main__":
    main()
