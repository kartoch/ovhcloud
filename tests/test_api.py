from unittest.mock import Mock

import ovh

from ovhcloud.client import OVHClient


def test_cache_command():
    ovh_client = Mock(ovh.Client)
    OVHClient(['cache'], ovh_client=ovh_client).action()
