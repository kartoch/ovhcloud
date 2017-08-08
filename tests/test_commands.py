import os
import tempfile

import pytest

from ovhcloud import cache
from ovhcloud.client import OVHClient


@pytest.mark.slow
def test_cache_command():
    temp_dir = tempfile.mkdtemp()
    OVHClient(['cache'], _configuration_dir=temp_dir).action()
    assert os.path.isfile(os.path.join(temp_dir, cache.ApiCacheCommand.DEFAULT_ENDPOINTS_CACHE_FILENAME))


def test_no_argument():
    temp_dir = tempfile.mkdtemp()
    with pytest.raises(SystemExit) as excinfo:
        OVHClient([], _configuration_dir=temp_dir).action()
    assert excinfo.value.code == 1


def test_version_command():
    with pytest.raises(SystemExit) as excinfo:
        OVHClient(['--version'], _configuration_dir=os.getcwd()).action()
    assert excinfo.value.code == 0
