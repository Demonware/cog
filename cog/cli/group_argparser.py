
# -*- coding: utf-8 -*-

import sys
import argparse

arg_no = len(sys.argv)
tool_parser = argparse.ArgumentParser(add_help=False)
tool_subparsers = tool_parser.add_subparsers(help='commands', dest='command')


# The edit command.
edit_parser = tool_subparsers.add_parser('edit', help='edit a POSIX group')
group0_parser = edit_parser.add_argument_group('user management')

group0_parser.add_argument(
  '--del-uid', action='append', dest='delMemberUid', metavar='<users to remove>'
)
group0_parser.add_argument(
  '--add-uid', action='append', dest='addMemberUid', metavar='<users to add>'
)
group0_parser = edit_parser.add_argument_group('group metadata')

group0_parser.add_argument(
  '--gid-number', action='store', dest='gidNumber', metavar='<new group ID>'
)
group0_parser.add_argument(
  '--description', action='store', dest='description', metavar='<group description>'
)
edit_parser.add_argument(
  '--type', '-t', choices=['generic', 'resource'], metavar='<type of group>', dest='group_type', default='generic', action='store'
)
edit_parser.add_argument(
  'cn', action='store', metavar='<group name>'
)

# The rename command.
rename_parser = tool_subparsers.add_parser('rename', help='change group name')
rename_parser.add_argument(
  'cn', action='store', metavar='<group name>'
)
rename_parser.add_argument(
  '--new-name', '-n', action='store', dest='newCn', metavar='<new group name>'
)

# The add command.
add_parser = tool_subparsers.add_parser('add', help='add a POSIX group')
add_parser.add_argument(
  '--type', '-t', choices=['generic', 'resource'], metavar='<type of group>', dest='group_type', default='generic', action='store'
)
add_parser.add_argument(
  'cn', action='store', metavar='<group name>'
)
group1_parser = add_parser.add_argument_group('additional arguments')

group1_parser.add_argument(
  '--gid-number', action='store', dest='gidNumber', metavar='<group id number>'
)
group1_parser.add_argument(
  '--with-uid', '-u', action='append', dest='memberUid', metavar='<users to add>'
)
group1_parser.add_argument(
  '--description', action='store', dest='description', metavar='<group description>'
)

# The remove command.
remove_parser = tool_subparsers.add_parser('remove', help='remove group from directory')
remove_parser.add_argument(
  'cn', action='store', metavar='<group name>'
)

# The show command.
show_parser = tool_subparsers.add_parser('show', help='show group details')
show_parser.add_argument(
  'cn', action='store', metavar='<group name>'
)

