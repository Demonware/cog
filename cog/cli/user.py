# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms


import sys
import getpass
import argparse
import yaml
import cog.util as util
import cog.directory as dir
from cog.objects.user import User
from cog.config import objects, Profiles

from user_argparser import tool_parser, arg_no

accounts = objects.get('accounts')
settings = Profiles().current()
user_rdn = settings.get('user_rdn')

def add_user(args, account_type):
    user_data = util.merge(accounts.get(account_type), args)
    if account_type in accounts.keys():
        name = user_data.pop('name')
        user_data[user_rdn] = name
        path = user_data.pop('path', None)
        groups = user_data.pop('group', None)
        requires = user_data.pop('requires', None)
        dn = "%s=%s,%s" % (user_rdn, name, dir.get_account_base(account_type))
        operator_uid = util.get_current_uid()
        for nameattr in ['cn', 'sn', 'givenName']:
            if not user_data.get(nameattr) and nameattr in requires:
                user_data[nameattr] = '%s (ask %s to fix me)' % (name, operator_uid)
        if not user_data.get('uid') and 'uid' in requires:
                user_data['uid'] = util.randomized_string(size=8)
        if not user_data.get('uidNumber') and 'uidNumber' in requires:
            user_data['uidNumber'] = dir.get_probably_unique_uidnumber()
        if not user_data.get('homeDirectory') and 'homeDirectory' in requires:
            user_data['homeDirectory'] = "/home/%s" % user_data['uid']

        user_data['userPassword'] = util.make_pass(user_data.get('userPassword'))

        user_entry = dir.Entry(dn=dn, attrs=user_data)
        newuser = User(name, user_entry, groups=groups)
        newuser.add()
    else:
        print "Account type %s is not exactly known." % account_type
        sys.exit(1)

def edit_user(args):
    replacable_attrs = ['uidnumber', 'gidnumber', 'sn', 'cn', 'givenname',
                        'homedirectory', 'loginshell', 'o', 'uid']
    appendable_attrs = ['addmail', 'addtelephonenumber']
    removable_attrs = ['delmail', 'deltelephonenumber']

    if user_rdn in args.keys():
        user = User(args.pop('name'), bind=True)
        user.rename(args.get(user_rdn))
        user = User(args.pop(user_rdn), bind=True)
    else:
        user = User(args.pop('name'), bind=True)

    if args.get('resetPassword'):
        del args['resetPassword']
        user.set_password(password=None)

    for attr, val in args.iteritems():
        attr = attr.lower()
        if attr in replacable_attrs:
            user.replace_item(attr, val)
        if attr in appendable_attrs:
            user.append_to_item(attr[3:], val)
        if attr in removable_attrs:
            user.remove_from_item(attr[3:], val)
        if attr == 'delgroup':
            for group in val:
                user.delgroup(group)
        if attr == 'addgroup':
            for group in val:
                user.addgroup(group)

    user.commit_changes()

def handle_types(args):
    if args.get('list_types'):
        print "Available account types:"
        for acc_type in sorted(accounts):
            print "  %s" % acc_type

def rename_user(args):
    user = User(args.get('name'), bind=True)
    user.rename(args.get('newName'))

def retire_user(name):
    user = User(name, bind=True)
    user.retire()

def remove_user(name):
    user = User(name, bind=True)
    user.remove()

def show_user(args):
    names = util.flatten_list(args.get('name'))
    tree = dir.Tree()
    query = '(&(objectClass=*)(%s=%s))'
    attrs = ['uid', 'cn', 'mail', 'title', 'o', 'uidNumber', 'gidNumber']
    if args.get('verbose'):
        attrs += ['objectClass', 'loginShell', 'homeDirectory', 'modifiersName', 'modifyTimestamp', 'sshPublicKeys']
    for name in names:
        search = tree.search(search_filter=(query % (user_rdn, name)), attributes=attrs)
        user = User(name)
        for item in search:
            groups = { 'groups': sorted(util.flatten_list([group for group in user.find_groups()])) }
            account = { name: util.merge(dict(item), groups) }
            print yaml.safe_dump(account, allow_unicode=True, default_flow_style=False)


def main():
    if arg_no < 2 or sys.argv[1] in ['-h', '--help']:
        print tool_parser.format_help()
        sys.exit(1)

    args = dict((k, v) for k, v in vars(tool_parser.parse_args()).iteritems() if v is not None)
    command = args.pop('command')
    account_type = args.pop('account_type', 'generic')

    if command == 'add':
        add_user(args, account_type)
    elif command == 'edit':
        edit_user(args)
    elif command == 'rename':
        rename_user(args)
    elif command == 'retire':
        retire_user(args.get('name'))
    elif command == 'remove':
        remove_user(args.get('name'))
    elif command == 'type':
        handle_types(args)
    elif command == 'show':
        show_user(args)

    sys.exit(0)

if __name__ == "__main__":
    main()
