cog
===

a flexible LDAP management tool

# Setup #

From the root of the source tree run:

    sudo python setup.py install --install-data=/

# Usage #

    cog --help
    cog [-p|--profile profile ] user --help
    cog [-p|--profile profile ] group --help
    cog [-p|--profile profile ] netgroup --help
    cog [-p|--profile profile ] access --help

The tool copies its configuration files into ~/.cog on first run; the
system-wide configuration is in /etc/cog, the settings are merged when
the tool is being run.

To start using the tool please either create a new profile similar to
the default (“local”) and set up is as default or simply edit the local
profile in the global settings file to your tastes.

List of available account types (roles) is available through

    cog user type -l

# Development #

Cog is a work in progress and still in an early stage of development
– feel free to request features and send patches. See the TODO.md file
for the list of the improvements that will be implemented first.

I'm trying to use the git-flow (in the avh flavour), see that you
either have the git-flow package installed or check out the
[gitflow-avh](https://github.com/petervanderdoes/gitflow) sources and
install the extension manually.

After cloning the repository for the first time, please run `sh flow-init`
– it will initialise git flow with the values I'm using.

# Known Bugs and Limitations #

* cog requires locale settings that use UTF-8
* error handling is abysmal, exceptions are thrown everywhere

# Testing #

To test you must also install the following dependencies:

* pytohn27-nose
* python27-mock

To run all tests, run the following in the root directory:

    nosetests-2.7
# Dependencies #

To install cog you need:

* pbr
* passlib
* python-setuptools
* python-ldap
* PyYAML

