import ovh
import pytest

from ovhcloud.client import OVHClient


def test_version_command():
    ovh_client = ovh.Client(endpoint='ovh-eu')
    with pytest.raises(SystemExit):
        OVHClient(['version'], ovh_client=ovh_client).action()
