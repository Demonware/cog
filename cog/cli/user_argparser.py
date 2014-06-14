
# -*- coding: utf-8 -*-

import sys
import argparse

arg_no = len(sys.argv)
tool_parser = argparse.ArgumentParser(add_help=False)
tool_subparsers = tool_parser.add_subparsers(help='commands', dest='command')


# The rename command.
rename_parser = tool_subparsers.add_parser('rename', help='rename an existing user account.')
rename_parser.add_argument(
  'name', action='store', metavar='<name>', help='account name'
)
rename_parser.add_argument(
  '--new-name', '-n', action='store', dest='newName', metavar='<new account name>'
)

# The add command.
add_parser = tool_subparsers.add_parser('add', help='add new user account to the directory.')
add_parser.add_argument(
  '--type', '-t', action='store', default='generic', dest='account_type', metavar='<type of account>'
)
add_parser.add_argument(
  'name', action='store', help='account name', metavar='<name>'
)
group1_parser = add_parser.add_argument_group('account specific')

group1_parser.add_argument(
  '--password', '-P', action='store', dest='userPassword', metavar='<account\'s owner password>'
)
group1_parser.add_argument(
  '--home', action='store', dest='homeDirectory', metavar='<path to the home directory>'
)
group1_parser.add_argument(
  '--shell', action='store', dest='loginShell', metavar='<path to the shell interpreter>'
)
group1_parser = add_parser.add_argument_group('personal information')

group1_parser.add_argument(
  '--phone-no', action='append', dest='telephoneNumber', metavar='<phone number>'
)
group1_parser.add_argument(
  '--last-name', action='store', dest='sn', metavar='<account owner\'s last name>'
)
group1_parser.add_argument(
  '--first-name', action='store', dest='givenName', metavar='<account owner\'s first name>'
)
group1_parser.add_argument(
  '--organization', '-o', action='store', dest='o', metavar='<organization>'
)
group1_parser.add_argument(
  '--email', action='append', dest='mail', metavar='<email>'
)
group1_parser.add_argument(
  '--full-name', action='store', dest='cn', metavar='<account owner\'s full name>'
)
group1_parser = add_parser.add_argument_group('uid and group management')

group1_parser.add_argument(
  '--uid', action='store', dest='uid', metavar='<user\'s uid>'
)
group1_parser.add_argument(
  '--add-group', action='append', dest='group', metavar='<secondary group>'
)
group1_parser.add_argument(
  '--uid-number', action='store', dest='uidNumber', metavar='<user id number>'
)
group1_parser.add_argument(
  '--gid', action='store', dest='gidNumber', metavar='<primary group id>'
)

# The show command.
show_parser = tool_subparsers.add_parser('show', help='show account data')
show_parser.add_argument(
  'name', action='append', nargs='*', help='account name'
)
show_parser.add_argument(
  '--verbose', '-v', action='store_true', dest='verbose', help='be verbose about it'
)

# The edit command.
edit_parser = tool_subparsers.add_parser('edit', help='edit existing user data in the directory')
edit_parser.add_argument(
  '--type', '-t', action='store', dest='account_type', metavar='<change account type>'
)
edit_parser.add_argument(
  'name', action='store', help='account name'
)
group1_parser = edit_parser.add_argument_group('account specific')

group1_parser.add_argument(
  '--reset-password', '-r', dest='resetPassword', action='store_true', help='<reset user\'s password>'
)
group1_parser.add_argument(
  '--home', action='store', dest='homeDirectory', metavar='<new home directory path>'
)
group1_parser.add_argument(
  '--shell', action='store', dest='loginShell', metavar='<new shell interpreter path>'
)
group1_parser = edit_parser.add_argument_group('personal information')

group1_parser.add_argument(
  '--first-name', action='store', dest='givenName', metavar='<new first name>'
)
group1_parser.add_argument(
  '--del-email', action='append', dest='delMail', metavar='<remove email address>'
)
group1_parser.add_argument(
  '--last-name', action='store', dest='sn', metavar='<new last name>'
)
group1_parser.add_argument(
  '--add-email', action='append', dest='addMail', metavar='<add new email address>'
)
group1_parser.add_argument(
  '--del-phone-no', action='append', dest='delTelephoneNumber', metavar='<phone number to remove>'
)
group1_parser.add_argument(
  '--organization', '-o', action='store', dest='o', metavar='<organization>'
)
group1_parser.add_argument(
  '--add-phone-no', action='append', dest='addTelephoneNumber', metavar='<phone number to add>'
)
group1_parser.add_argument(
  '--full-name', action='store', dest='cn', metavar='<new full name>'
)
group1_parser = edit_parser.add_argument_group('uid and group management')

group1_parser.add_argument(
  '--del-group', action='append', dest='delgroup', metavar='<remove user from the group>'
)
group1_parser.add_argument(
  '--group-id', action='store', dest='gidNumber', metavar='<change primary group ID>'
)
group1_parser.add_argument(
  '--add-group', action='append', dest='addgroup', metavar='<add user to the group>'
)
group1_parser.add_argument(
  '--uid-number', action='store', dest='uidNumber', metavar='<change user ID number>'
)
group1_parser.add_argument(
  '--uid', action='store', dest='uid', metavar='<user\'s uid>'
)

# The retire command.
retire_parser = tool_subparsers.add_parser('retire', help='retire an existing account and remove all its privileges.')
retire_parser.add_argument(
  'name', action='store', metavar='<name>', help='account name'
)

# The type command.
type_parser = tool_subparsers.add_parser('type', help='manage user types')
type_parser.add_argument(
  '--list', '-l', action='store_true', dest='list_types', help='list user types'
)

# The remove command.
remove_parser = tool_subparsers.add_parser('remove', help='remove an existing account.')
remove_parser.add_argument(
  'name', action='store', metavar='<name>', help='account name'
)

