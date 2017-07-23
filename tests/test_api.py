import pytest

from ovhcloud.client import OVHClient


def test_cache_command():
    with pytest.raises(SystemExit):
        OVHClient(['cache']).action()
