from unittest import mock

from ovhcloud.client import OVHClient


@mock.patch('ovh.Client.get')
def test_me_command(ovh_client_get):
    c = OVHClient(['me'])
    c.action()
    ovh_client_get.assert_called_with('/me')


def test_version_command():
    OVHClient(['version'])


@mock.patch('ovh.Client.get')
def test_ssh_group(ovh_client_get):
    c = OVHClient(['ssh'])
    c.action()
    ovh_client_get.assert_called_with('/me/sshKey')

#     c = OVHClient(['ssh', 'add', 'myname', 'mykey'])
#     c.action()
#     c = OVHClient(['ssh', 'rm', 'myname'])
#     c.action()
