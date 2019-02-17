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
  As knxd is only part of ebian beginnning with Debian 10 (buster)
  this one does not test against older Debian releases.
  But role should work there as well if user provides custom repository
  with ready-made deb-packages.
  Furthermore this scenario tests integration into "monit" for monitoring
  the knxd daemon.  
  
  _This one is not working right now due to some connection errorswith buster image!_

