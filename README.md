Role "sseide.knxd"
=========

This role installs KNXD daemon either from existing deb repository or by compiling source code
to build new debian packages.

KNXD source code can be found at https://github.com/knxd/knxd

Requirements
------------

This role does not need any other dependencies than Ansible itself.
If daemon is compiled from source all packages needed are installed by the role itself.


Role Variables
--------------

A description of the settable variables for this role should go here, including
any variables that are in defaults/main.yml, vars/main.yml, and any variables
that can/should be set via parameters to the role. Any variables that are read
from other roles and/or the global scope (ie. hostvars, group vars, etc.) should
be mentioned here as well.

Dependencies
------------

This role does not depend on other roles.

Example Playbook
----------------

Minimal example to install already existing knxd packages from a repository available
to the managed host.

    - hosts: servers
      roles:
         - { role: sseide.knxd }

Example to install knxd from source via checkout from github and compiling afterwards.
The optional version can be either an GitHub TAG name or a branch

    - hosts: servers
      roles:
         - { role: sseide.knxd, knxd_source_compile: false }

    - hosts: servers
      roles:
         - { role: sseide.knxd, knxd_source_compile: false, knxd_source_version: "v0.14.25" }


License
-------

MIT

Author Information
------------------

This role was created in 2018 by Stefan Seide
