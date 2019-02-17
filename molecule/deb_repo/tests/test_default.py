import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_knxd_is_installed(host):
    knxd = host.package('knxd')
    assert knxd.is_installed


def test_knxdtools_is_installed(host):
    knxd = host.package('knxd-tools')
    assert knxd.is_installed


def test_knxd_conf_file(host):
    f = host.file('/etc/knxd.conf')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_knxd_ini_file(host):
    f = host.file('/etc/knxd.ini')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_defaults_knxd_file(host):
    f = host.file('/etc/default/knxd')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_knxd_service_file(host):
    f = host.file('/lib/systemd/system/knxd.service')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_knxd_is_running(host):
    knxd = host.service('knxd')
    assert knxd.is_running
    assert knxd.is_enabled
