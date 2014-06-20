# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms


import sys
import getpass
import argparse
import cog.util as util
import cog.directory as dir
from cog.objects.netgroup import Netgroup, make_triple
from cog.config import objects, Profiles

from access_argparser import tool_parser, arg_no

netgroups = objects.get('netgroups')
settings = Profiles().current()
(granted, denied) = (True, False)

def get_access_group(name, access_type=granted):
    """
    Gets a netgroup handle. Creates the group when necessary.
    """
    group_type = 'security'
    group_data = util.merge(netgroups.get(group_type), {})
    path = group_data.pop('path')
    requires = group_data.pop('requires')
    if access_type:
        group_name = '%s-granted' %(name)
        description = 'Users allowed to access %s.' % name
    else:
        group_name = '%s-denied' % (name)
        description = 'Users denied access to %s.' % name

    dn = 'cn=%s,%s' % (group_name, dir.get_netgroup_base(group_type))
    access_group = Netgroup(group_name, dir.Entry(dn=dn, attrs=group_data, use_dn=True))
    if not access_group.exists:
        access_group.add()
        access_group.set_description(description)
    return access_group

def grant_access(args):
    for access_object in util.flatten_list(args.get('host', []) + args.get('service', [])):
        access_group = get_access_group(access_object.lower())
        for uid in util.flatten_list(args.get('uid')):
            access_group.add_triple([make_triple(None, uid, None)])
        access_group.commit_changes()

def deny_access(args):
    for access_object in util.flatten_list(args.get('host', []) + args.get('service', [])):
        access_group = get_access_group(access_object.lower(), access_type=denied)
        for uid in util.flatten_list(args.get('uid')):
            access_group.add_triple(make_triple(None, uid, None))
        access_group.commit_changes()

def revoke_access(args):
    access_type = granted
    revoke_type = args.pop('revoke_type')
    if revoke_type == 'deny':
        access_type = denied
    for access_object in util.flatten_list(args.get('host', []) + args.get('service', [])):
        access_group = get_access_group(access_object.lower(), access_type)
        for uid in util.flatten_list(args.get('uid')):
            access_group.del_triple(make_triple(None, uid, None))
            access_group.commit_changes()

def show_access(args):
    tree = dir.Tree()
    access_types = ['denied', 'granted']
    if args.get('query_type') in ['host', 'service']:
        # make sure that the netgroup actually contains any triples:
        query = '(&(objectClass=nisNetgroup)(cn=%s-%s)(nisNetgroupTriple=*))'
        for access_type in access_types:
            for access_object in args.get('query'):
                search = tree.search(search_filter=(query % (access_object, access_type)), attributes=['cn', 'nisNetgroupTriple'])
                if search:
                    users = [x.strip('(-,)') for x in search[0]['nisNetgroupTriple']]
                    print '%s at %s: %s' % (access_type, access_object, ', '.join(users))
    elif args.get('query_type') == 'user':
        uids = args.get('query')
        access_list = dict((k, dict(zip(access_types, (set(), set())))) for k in uids)
        query_uids = ''.join(['(nisNetgroupTriple=*,%s,*)' % uid for uid in uids])
        if len(uids) > 1:
            query_uids = '(|' + query_uids + ')'
        query = '(&(objectClass=nisNetgroup)(cn=*-*)%s)' % query_uids
        for netgroup_entry in tree.search(search_filter = query, attributes=['cn', 'nisNetgroupTriple']):
            access_object, access_type = netgroup_entry.get('cn')[0].split('-')
            access_uids = [x.strip('(-,)') for x in netgroup_entry.get('nisNetgroupTriple')]
            for uid in uids:
                if uid in access_uids:
                    access_list[uid][access_type].add(access_object)
        for uid, access_types in access_list.iteritems():
            for access_type, access_objects in access_types.iteritems():
                if access_objects:
                    print '%s %s on %s' % (uid, access_type, ", ".join(sorted(access_objects)))

def main():
    if arg_no < 2 or sys.argv[1] in ['-h', '--help']:
        print tool_parser.format_help()
        sys.exit(1)

    args = dict((k, v) for k, v in vars(tool_parser.parse_args()).iteritems() if v is not None)
    command = args.pop('command')
    netgroup_type = args.pop('netgroup_type', 'generic')

    if command == 'grant':
        grant_access(args)
    elif command == 'deny':
        deny_access(args)
    elif command == 'revoke':
        revoke_access(args)
    elif command == 'show':
        show_access(args)

    sys.exit(0)

if __name__ == '__main__':
    main()
