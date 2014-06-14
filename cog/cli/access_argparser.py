
# -*- coding: utf-8 -*-

import sys
import argparse

arg_no = len(sys.argv)
tool_parser = argparse.ArgumentParser(add_help=False)
tool_subparsers = tool_parser.add_subparsers(help='commands', dest='command')


# The deny command.
deny_parser = tool_subparsers.add_parser('deny', help='deny access to user(s) at specified host(s)')
deny_parser.add_argument(
  '--on-host', '-H', action='append', dest='host', nargs='+', metavar='<host name>'
)
deny_parser.add_argument(
  '--on-service', '-s', action='append', dest='service', nargs='+', metavar='<service short name>'
)
deny_parser.add_argument(
  '--to-user', '-u', action='append', dest='uid', nargs='+', metavar='<user name>'
)

# The grant command.
grant_parser = tool_subparsers.add_parser('grant', help='grant access to user(s) at specified host(s)')
grant_parser.add_argument(
  '--on-host', '-H', action='append', dest='host', nargs='+', metavar='<host name>'
)
grant_parser.add_argument(
  '--on-service', '-s', action='append', dest='service', nargs='+', metavar='<service short name>'
)
grant_parser.add_argument(
  '--to-user', '-u', action='append', dest='uid', nargs='+', metavar='<user name>'
)

# The revoke command.
revoke_parser = tool_subparsers.add_parser('revoke', help='revoke access grant or denial')
revoke_parser.add_argument(
  '--on-host', '-H', action='append', dest='host', nargs='+', metavar='<host name>'
)
revoke_parser.add_argument(
  '--on-service', '-s', action='append', dest='service', nargs='+', metavar='<service short name>'
)
revoke_parser.add_argument(
  '--type', '-t', choices=['grant', 'deny'], metavar='<access type>', default='grant', dest='revoke_type', action='store'
)
revoke_parser.add_argument(
  '--from-user', '-u', action='append', dest='uid', nargs='+', metavar='<user name>'
)

# The show command.
show_parser = tool_subparsers.add_parser('show', help='show access details for user(s) or host(s)')
show_parser.add_argument(
  'query', nargs='+', help='<hosts, users or services>'
)
show_parser.add_argument(
  '--type', '-t', choices=['user', 'host', 'service'], action='store', dest='query_type'
)

