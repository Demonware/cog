# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms


import sys
import getpass
import argparse
import cog.util as util
import cog.directory as dir
from cog.objects.netgroup import Netgroup
from cog.config import objects, Profiles

from netgroup_argparser import tool_parser, arg_no

netgroups = objects.get('netgroups')
settings = Profiles().current()

def add_netgroup(args, netgroup_type):
    netgroup_data = util.merge(netgroups.get(netgroup_type), args)
    if netgroup_type in netgroups.keys():
        cn = netgroup_data.get('cn')
        path = netgroup_data.pop('path', None)
        requires = netgroup_data.pop('requires', None)
        dn = "cn=%s,%s" % (cn, dir.get_netgroup_base(netgroup_type))
        netgroup_entry = dir.Entry(dn=dn, attrs=netgroup_data)
        newnetgroup = Netgroup(cn, netgroup_entry)
        newnetgroup.add()
    else:
        print "Netgroup type %s is not exactly known." % netgroup_type
        sys.exit(1)

def edit_netgroup(args):
    netgroup = Netgroup(args.pop('cn'))
    for attr, val in args.iteritems():
        attr = attr.lower()
        if attr == 'description':
            netgroup.set_description(val)
        elif attr == 'addnetgrouptriple':
            netgroup.add_triple(val)
        elif attr == 'delnetgrouptriple':
            netgroup.del_triple(val)
    netgroup.commit_changes()

def rename_netgroup(args):
    netgroup = netgroup(args.get('cn'))
    netgroup.rename(args.get('newCn'))

def remove_netgroup(cn):
    netgroup = netgroup(cn)
    netgroup.remove()

def main():
    if arg_no < 2 or sys.argv[1] in ['-h', '--help']:
        print tool_parser.format_help()
        sys.exit(1)

    args = dict((k, v) for k, v in vars(tool_parser.parse_args()).iteritems() if v is not None)
    command = args.pop('command')
    netgroup_type = args.pop('netgroup_type', 'generic')

    if command == 'add':
        add_netgroup(args, netgroup_type)
    elif command == 'edit':
        edit_netgroup(args)
    elif command == 'rename':
        rename_netgroup(args)
    elif command == 'remove':
        remove_netgroup(args.get('cn'))

    sys.exit(0)

if __name__ == "__main__":
    main()
