
# -*- coding: utf-8 -*-

import sys
import argparse

arg_no = len(sys.argv)
tool_parser = argparse.ArgumentParser(add_help=False)
tool_subparsers = tool_parser.add_subparsers(help='commands', dest='command')


# The edit command.
edit_parser = tool_subparsers.add_parser('edit', help='edit a netgroup')
group0_parser = edit_parser.add_argument_group('user management')

group0_parser.add_argument(
  '--del-triple', action='append', dest='delNisNetgroupTriple', metavar='<triples to remove>'
)
group0_parser.add_argument(
  '--add-triple', action='append', dest='addNisNetgroupTriple', metavar='<triples to add>'
)
group0_parser.add_argument(
  '--description', action='store', dest='description', metavar='<netgroup description>'
)
edit_parser.add_argument(
  'cn', action='store', metavar='<group name>'
)

# The rename command.
rename_parser = tool_subparsers.add_parser('rename', help='change netgroup name')
rename_parser.add_argument(
  'cn', action='store', metavar='<netgroup name>'
)
rename_parser.add_argument(
  '--new-name', '-n', action='store', dest='newCn', metavar='<new netgroup name>'
)

# The add command.
add_parser = tool_subparsers.add_parser('add', help='add a netgroup')
add_parser.add_argument(
  'cn', action='store', metavar='<netgroup name>'
)
group1_parser = add_parser.add_argument_group('additional arguments')

group1_parser.add_argument(
  '--with-triples', '-t', action='append', dest='nisNetgroupTriple', metavar='<netgroup triples to add>'
)
group1_parser.add_argument(
  '--description', action='store', dest='description', metavar='<netgroup description>'
)

# The remove command.
remove_parser = tool_subparsers.add_parser('remove', help='remove netgroup')
remove_parser.add_argument(
  'cn', action='store', metavar='<netgroup name>'
)

