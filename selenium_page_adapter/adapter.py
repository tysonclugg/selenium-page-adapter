"""Selenium Page Adapter."""
from selenium import webdriver
import logging


logger = logging.getLogger(__name__)


class DeferredPageSource(object):

    """Wrapper to allow deferred retrieval of driver.page_source."""

    def __init__(self, driver):
        """Stash reference to driver for later use."""
        self.driver = driver

    def __repr__(self):
        """Return repr of driver.page_source."""
        return repr(self.driver.page_source)

    def __str__(self):
        """Return driver.page_source."""
        return self.driver.page_source


class PageAdapter(object):

    """Page adapter base class."""

    def __init__(self, driver, el=None):
        """Stash context and driver for later use."""
        self.driver = driver
        self.page_source = DeferredPageSource(driver)
        if el is None:
            self.el = driver
        else:
            self.el = el

    def get_url(self):
        """Get current page address."""
        return self.driver.current_url

    def set_url(self, path):
        """Set current page address (can be absolute or relative)."""
        self.driver.get(path)

    url = property(get_url, set_url)

    def fill(self, el, text):
        """Fill specified form element with text."""
        webdriver.ActionChains(
            self.driver,
        ).move_to_element(el).click().perform()
        el.clear()
        el.send_keys(text)
        assert el.get_attribute('value') == text, \
            '%r not set in %r' % (text, el)
