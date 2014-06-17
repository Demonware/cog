#/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, Activision Publishing, Inc.

# the cog project is free software under 3-clause BSD licence
# see the LICENCE file in the project root for copying terms

import sys, os, re, shutil
import argparse
from importlib import import_module
from cog.config import Profiles

path = os.path.dirname(os.path.abspath(__file__))

def find_subcommands():
    for filename in os.listdir(path + os.sep + 'cli'):
        name, ext = os.path.splitext(filename)
        if ext.endswith('.py') and not (name.endswith('_argparser') or name == '__init__'):
            yield name

def run(command):
    module = 'cog.cli.%s' % command
    command = import_module(module)
    sys.exit(command.main())

def usage(commands, profiles):
    print 'cog, a flexible LDAP directory manager'
    print
    print 'Usage: cog [-p|--profile <profile>] [-h|--help] command [options]'
    print '       for more details run ‘cog command --help’ and'
    print '                            ‘cog command subcommand --help’'
    print '       available profiles: %s and %s.' % (', '.join(profiles[:-1]), profiles[-1])
    print '       available commands: %s and %s.' % (', '.join(commands[:-1]), commands[-1])
    print
    print 'Command summary:'
    parser = dict()
    for command in commands:
        parser[command] = __import__('cog.cli.%s_argparser' % command, globals(), locals(), ['tool_parser']).tool_parser
        parser[command].prog = 'cog %s' % command
        parser[command].add_help = False
        print parser[command].format_usage()[6:-1]
    print

def make_user_config():
    user_dir = os.environ['HOME'] + os.sep + '.cog'
    conf_dir = '/etc/cog'
    if not os.path.exists(user_dir):
        os.makedirs(user_dir, mode=0750)
        shutil.copyfile(conf_dir + os.sep + 'examples/settings.local', user_dir + os.sep + 'settings')

def main():
    profiles = Profiles()
    make_user_config()

    subcommands = [command for command in find_subcommands()]

    partial_parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    partial_parser.add_argument("-p", "--profile", choices=profiles.list(), dest="profile")
    args, remaining = partial_parser.parse_known_args()
    profiles.use(args.profile)
    if remaining:
        command = remaining.pop(0)
        sys.argv = ['cog %s' % command] + remaining
    if len(sys.argv) < 2:
        usage(subcommands, profiles.list())
    else:
        if command in subcommands:
            run(command)

if __name__ == '__main__':
    main()
