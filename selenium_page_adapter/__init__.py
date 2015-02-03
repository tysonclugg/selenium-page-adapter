"""Selenium Page Adapter."""
import os
from pkg_resources import get_distribution, DistributionNotFound
from .descriptors import ElementDescriptor, AllElements, AvailableElements
from .adapter import PageAdapter


try:
    _dist = get_distribution('selenium_page_adapter')
    if not __file__.startswith(os.path.join(_dist.location, 'selenium_page_adapter', '')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'development'
else:
    __version__ = _dist.version
