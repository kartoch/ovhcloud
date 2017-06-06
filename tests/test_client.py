from ovhcloud.client import OVHClient


def test_version_command():
    OVHClient(['version'])
