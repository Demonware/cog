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

To start using cog with our infrastructure you need to change the
profile in the settings file to 'shared' and configure `bind_dn` option
using your full DN.

List of available account types (roles) is available through `cog user
type -l`.

# Known Bugs and Limitations #
* cog requires locale settings that use UTF-8
* error handling is abysmal, exceptions are thrown everywhere

# Dependencies #

To install cog you need:

* pbr
* passlib
* python-setuptools
* python-ldap
* PyYAML

