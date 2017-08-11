import logging
import os

from pkg_resources import get_distribution, resource_filename

__version__ = get_distribution('ovhcloud').version

DEFAULT_CONFIGURATION_DIR = os.path.expanduser('~/.ovhcloud/')

DEFAULT_ENDPOINTS_CACHE_FILENAME = 'endpoints_cache.json'

DEFAULT_ENDPOINTS_API_CACHE = resource_filename('ovhcloud', DEFAULT_ENDPOINTS_CACHE_FILENAME)

logging.getLogger(__name__).addHandler(logging.NullHandler())
