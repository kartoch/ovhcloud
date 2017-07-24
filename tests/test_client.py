try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import ovh

from ovhcloud.client import OVHClient


def test_version_command():
    ovh_client = Mock(ovh.Client)
    OVHClient(['version'], ovh_client=ovh_client).action()
