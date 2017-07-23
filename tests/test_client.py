import pytest

from ovhcloud.client import OVHClient


def test_version_command():
    with pytest.raises(SystemExit):
        OVHClient(['version']).action()
