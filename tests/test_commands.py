import os
import tempfile

import pytest

import ovhcloud
from ovhcloud.client import OVHClient


@pytest.mark.slow
def test_cache_command():
    temp_dir = tempfile.mkdtemp()
    OVHClient(['cache'], _configuration_dir=temp_dir).action()
    assert os.path.isfile(os.path.join(temp_dir, ovhcloud.DEFAULT_ENDPOINTS_CACHE_FILENAME))


def test_no_argument():
    with pytest.raises(SystemExit) as excinfo:
        OVHClient([]).action()
    assert excinfo.value.code == 1


def test_version_command():
    with pytest.raises(SystemExit) as excinfo:
        OVHClient(['--version']).action()
    assert excinfo.value.code == 0
