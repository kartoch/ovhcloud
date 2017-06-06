import logging

from pkg_resources import get_distribution

__version__ = get_distribution('ovhcloud').version

logging.getLogger(__name__).addHandler(logging.NullHandler())
