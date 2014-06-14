cog
===

a flexible LDAP management tool

# Setup #

From the root of the source tree run:

    sudo python setup.py install

If you see any errors regarding certificates or server connection,
remove the /etc/cog directory and run setup.py as root again.

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
profile in the settings file to 'shared' and configure bind_dn option
using your full DN.

List of available account types (roles) is available through ``cog user
type -l``.

# Known Bugs and Limitations #

* cog requires an UTF-8 locale
* error handling is abysmal, cog throws exceptions everywhere.

# Dependencies #

To install cog you need:

* python-setuptools
* python-ldap
* PyYAML

