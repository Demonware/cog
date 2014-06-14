#!/usr/bin/env python

from setuptools import setup, find_packages

setup (
    name = 'cog',
    description = 'configurable command-line LDAP directory manager',
    author = 'Miroslaw Baran',
    author_email = 'miroslaw@demonware.net',
    version = '1.0',
    scripts = ['bin/cog'],
    data_files = [
        ('/etc/cog', ['config/settings', 'config/templates.yaml']),
        ('/etc/cog/examples', ['config/settings.local'])
    ],
    package_data = {'cog': ['*.yaml']},
    packages = find_packages(),
    install_requires = ['passlib', 'python-ldap', 'pyyaml'],
    zip_safe = False,
)
