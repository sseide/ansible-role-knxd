Role "sseide.knxd"
=========

[![Ansible Role](https://img.shields.io/ansible/role/35936.svg)](https://img.shields.io/ansible/role/35936.svg)
[![Build Status](https://travis-ci.org/sseide/ansible-role-knxd.svg?branch=master)](https://travis-ci.org/sseide/ansible-role-knxd)
[![Version](https://img.shields.io/github/tag/sseide/ansible-role-knxd.svg)](https://img.shields.io/github/tag/sseide/ansible-role-knxd.svg)
[![Code Quality](https://img.shields.io/ansible/quality/35936.svg)](https://img.shields.io/ansible/quality/35936.svg)

This role installs KNXD daemon either from packages at an existing debian repository
or by compiling the source code from git repo to build new debian packages.

KNXD source code can be found at https://github.com/knxd/knxd

This role creates a knxd.ini file for usage with external KNX IP-Interfaces, IP-Routers
or TPUART devices.
 
For using KNXD with a `USB` driver or other usages you should provide your own knxd.ini template file 
and not the one provided with this role. In this case just set the
`knxd_config_file` variable to your own template.


Requirements
------------

This role does not need any other dependencies than Ansible itself (and a KNX installation to speak with of course...).

If daemon is compiled from source all packages needed are installed by the role itself.
Compiling from source is only tested with latest 0.14.x releases, as knxd.ini file 
used by this role was introduced then.

When packages shall be installed from existing debian repository please make shure
package is available. `knxd` is part of Debian main repository starting with Debian 9 "Buster".
For installation at older Debian releases please provide your own debian repository
(e.g. with reprepro) and make shure this one is already added to the systems apt sources.  

Role Variables
--------------

All values given for the role parameters are the default values as defined in
`defaults/main.yml` and `vars/main.yml`.

---

Compile from github sources (true) or install from some debian repository via `apt-get install` (false).
If compile from source is true the explicit version to check out can be set too.
The version name can be either a github tag or branch name, e.g. "DEBIAN-0.14.29-3", "v0.14.25", ...
```
knxd_source_compile: false
knxd_source_version: "DEBIAN-0.14.29-3"
```
If code is compiled from source this flag defines if already build deb packages shall be
reused on additional runs or if code should be recompiled every time.
```
knxd_source_force_rebuild: false
```

Set to true to install template for monitoring of the knxd server via 'Monit' (http://www.tildeslash.com/monit)
The 'monit' package must already be installed
```
knxd_use_monit: false
```

Install knxd-dev debian packages or packages with debug symbols too? defaults to false
```
knxd_install_dev_package: false
knxd_install_debug_package: false
```

This role can either use its own template to create an knxd.ini file (default value)
or you can set the path to your own template files to create a more sophisistcateds
version of the ini file not possible with the default template.
If the default template is used all of the followinf `knxd_arg_` config parameters 
below can be used to configure the knxd.ini file created
```
knxd_config_file: "templates/knxd.ini"
```

#### Config parameter used in roles default ini template

List of Knxd command line params to configure different drivers.
Each list entry describes one driver, the attribute "driver" must exist for each entry
with the name of the driver (e.g. `ip`, `ipt`, `tpuart`).
Only supported drivers are ip, ipt and tpuart with options and optional filters.

Example:
```yaml
knxd_arg_drivers:
  - driver: "dummy"
  - driver: "ip"
    ipaddr: "224.2.3.4"      # (optional) translated to multicast-address used
    filters: "single,retry"
  - driver: "ipt"
    ipaddr: "8.7.6.5"        # translated to ip tunneling gateways ip-address
    filters:
      - single
      - retry
  - driver: "tpuart"
    device: "/dev/bla/blub"  # name of local device
    baudrate: 28800          # (optional) speed used talking to this device
```

Other drivers will work when they do not need any driver specific options (like `dummy` driver).
Only filters are supported than.
Default Value is:
```
knxd_arg_drivers:
  - driver: "dummy"
```

KNX/EIB address (param -e)
```
knxd_arg_eib_addr: "0.0.1"
```

KNX/EIB client addresses (param -E)
```
knxd_arg_eib_client_addr: "0.0.2:8"
```

Path to local listener socket
```
knxd_arg_local_socket: "/var/run/knx"
```

Local tcp port to listen on
```
knxd_arg_local_port: 6270
```

Template for knxd connection string, depends on local socket and port configured
```
knxd_arg_connection: "{% if knxd_arg_local_socket %}B.unix,{% endif %}{% if knxd_arg_local_port %}C.tcp,{% endif %}{% if knxd_arg_driver %}D.ipt{% endif %}"
```

#### Other default variables
The following variables should not be changed for normal operations.

This variable lists all tools (packages) needed to compile the source code.
They will be installed only if knxd will be compiled by itself.
```
knxd_build_tools:
  - git-core
  - build-essential
  - debhelper
  - autotools-dev
  - autoconf
  - automake
  - libtool
  - pkg-config
  - dh-systemd
```

These are the development versions of the libraries needed for knxd version 0.14.25.
If another version is compiled and compilation fails with missing tools, they should be added here.

`libsystemd-daemon-dev` is not needed anymore on Debian Stretch and newer, it will be 
automatically removed by this role if necessary. It must be listed here to be compatible 
with Debian Jessie.
```
knxd_build_libs_dev:
  - libusb-1.0-0-dev
  - libsystemd-dev
  - libsystemd-daemon-dev
  - libev-dev
  - cmake
```



Dependencies
------------

This role does not depend on other roles.

Example Playbook
----------------

#### Minimal Example, Installation from Debian Repository
Minimal example to install already existing knxd packages from a repository available
to the managed host.

    - hosts: servers
      roles:
         - { role: sseide.knxd }

The knxd.ini configuration created looks like the following:
```ini

```

#### Minimal Example, Installation via GIT checkout and compilation

Example to install knxd from source via checkout from github and compiling afterwards.
The optional version can be either an GitHub TAG name or a branch

    - hosts: servers
      roles:
         - { role: sseide.knxd, knxd_source_compile: true }

    - hosts: servers
      roles:
         - { role: sseide.knxd, knxd_source_compile: true, knxd_source_version: "v0.14.25" }

#### Example with two drivers: IPT and TPUART

The following example configures two different drivers to use, one using
IP-Tunneling to the remote ip address 192.168.8.8 and one USB-Device at /dev/ttyACM0 
using the TPUART driver with a baud rate of 28.800.

    - hosts: servers
      roles:
         - role: sseide.knxd
           knxd_arg_drivers:
             - driver "ipt"
               ipaddr: "192.168.8.8"
               filters:
                 - single
                 - retry
             - driver: "tpuart"
               device: "/dev/ttyACM0"
               baudrate: 28800
               filters: "single,retry" 

Optional filters can be assigned to all drivers. Filters can be added as a string written
into the ini file as is or as a yaml list of filters

#### Example with custom knxd.ini file

The following example does not use the knxd.ini template provided by this role.
Here your own file (either plain file or jinja2 template) `files/myknxd.ini`
is used to render the knxd.ini configuration file.

    - hosts: servers
      roles:
         - role: sseide.knxd
           knxd_config_file: 'files/myknxd.ini'

Using your own file the following role variables are not used anymore:
```yaml
knxd_arg_drivers
knxd_arg_eib_addr
knxd_arg_eib_client_addr
knxd_arg_connection
```

The following vars are only used if target system has systemd running:
```yaml
knxd_arg_local_socket
knxd_arg_local_port
```

License
-------

MIT

Author Information
------------------

This role was created in 2018-2019 by Stefan Seide
