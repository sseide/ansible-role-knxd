Role "sseide.knxd"
=========

This role installs KNXD daemon either from packages at an existing debian repository
or by compiling the source code from git repo to build new debian packages.

KNXD source code can be found at https://github.com/knxd/knxd

This role creates a knxd.ini file for usage with an external KNX IP-Interface or IP-Router. 
For using KNXD with a USB-to-KNX Interface or other usages you should use your own knxd.ini template file 
and not the one provided with this role. In this case just set the
`knxd_config_file` variable to your own template.


Requirements
------------

This role does not need any other dependencies than Ansible itself (and a KNX installation to speak with of course...).
If daemon is compiled from source all packages needed are installed by the role itself.


Role Variables
--------------

All values given for the role parameters are the default values as defined in
`defaults/main.yml` and `vars/main.yml`.

---

compile from github sources (true) or install from some debian repository via `apt-get install` (false).
If compile from source is true the explicit version to check out can be set too.
The version name can be either a github tag or branch name, e.g. "DEBIAN-0.14.27-2", "v0.14.25", ...
```
knxd_source_compile: false
knxd_source_version: "v0.14.25"
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

Knxd command line param to select driver (param -b).
Possible values supported are `""` (empty string), `ipt` or `ip`
```
knxd_arg_driver: "ipt"
```

This is the ip address or broadcast address, depending on driver used above (ip|ipt)
```
knxd_arg_ipgw: "192.168.1.8"
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


License
-------

MIT

Author Information
------------------

This role was created in 2018 by Stefan Seide
