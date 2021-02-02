## Automated role tests with molecule

There are two scenarios defined for testing with molecule:

Running test:

* `molecule test` - test default scenario only
* `molecule test --scenario-name deb_repo` - test specific scenario only
* `molecule test --all` - test all scenarios

### _default_

  This one gets sorce from github, compiles and installs knxd
  Tested against Debian 8 (jessie) and Debian 9 (stretch)
  
### _deb_repo_
  
  This one installs precompiled packages from debian repository.
  As knxd is only part of Debian starting with Debian 10 (buster)
  this one does not test against older Debian releases.
  This role should work there as well if user provides a custom repository
  with ready-made deb-packages.
  Furthermore, this scenario tests integration into "monit" for monitoring
  the knxd daemon.  
  
  _This one is not working right now due to some connection errors with buster image!_

## Installation / Setup of molecule

* create python venv to install molecule (downloads entire ansible and so on)
```shell script
$ cd <project-dir>
$ python3 -m venv molecule-venv
$ source molecule-venv/bin/activate
(molecule-venv) $ pip install "molecule[lint]"
```
Debian needs package "python3-venv" for this.

Before running molecule commands and test - activate it:
```shell script
$ cd <project-dir>
$ source molecule-venv/bin/activate
```

## Code Linting

```shell script
$ molecule lint
```
