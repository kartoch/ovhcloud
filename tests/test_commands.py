import os
from shutil import copyfile

from ovhcloud import cache
from ovhcloud.client import OVHClient

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

import tempfile


def test_cache_command_with_cached_file():
    temp_dir = tempfile.mkdtemp()
    copyfile(cache.ApiCacheCommand.DEFAULT_ENDPOINTS_CACHE_FILENAME,
             os.path.join(temp_dir, cache.ApiCacheCommand.DEFAULT_ENDPOINTS_CACHE_FILENAME))
    assert not OVHClient(['cache'], _configuration_dir=temp_dir).action()


def test_cache_command_without_cached_file():
    temp_dir = tempfile.mkdtemp()
    assert OVHClient(['cache'], _configuration_dir=temp_dir).action()
    assert os.path.isfile(os.path.join(temp_dir, cache.ApiCacheCommand.DEFAULT_ENDPOINTS_CACHE_FILENAME))


def test_version_command():
    OVHClient(['version']).action()
