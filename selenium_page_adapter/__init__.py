"""Selenium Page Adapter."""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


class ElementDescriptor(object):

    """Data descriptor to ease getting specified element when required."""

    def __init__(self, by, selector):
        """Stash our function to find element by selector args."""
        self.by = by
        self.selector = selector

    def __get__(self, obj, cls=None):
        """Return our element if displayed."""
        # wait for element to exist
        el = WebDriverWait(obj.driver, 5).until(
            method=lambda drv: drv.find_element(self.by, self.selector),
            message='Element with %r = %r not found.' % (
                self.by,
                self.selector,
            ),
        )
        # now it exists, wait for it to become visible as per the W3C spec:
        # http://www.w3.org/TR/webdriver/#determining-visibility
        WebDriverWait(obj.driver, 5).until(
            method=lambda drv: el.is_displayed(),
            message='Element with %r = %r is not displayed.' % (
                self.by,
                self.selector,
            ),
        )
        # element is now visible somewhere on the page, move mouse over it.
        webdriver.ActionChains(obj.driver).move_to_element(el)
        return el


class AllElements(object):

    """Data descriptor to ease getting elements as dict."""

    def __init__(self, el_to_key, by, selector):
        """Stash our function to generate keys and by selector args."""
        self.el_to_key = el_to_key
        self.by = by
        self.selector = selector

    def __get__(self, obj, cls=None):
        """Generate dict of items."""
        return {
            self.el_to_key(el): el
            for el
            in obj.driver.find_elements(self.by, self.selector)
        }


class AvailableElements(object):

    """Data descriptor to ease getting available elements as dict."""

    def __init__(self, el_to_key, by, selector):
        """Stash our function to generate keys and by selector args."""
        self.el_to_key = el_to_key
        self.by = by
        self.selector = selector

    def __get__(self, obj, cls=None):
        """Generate dict of available items."""
        return {
            self.el_to_key(el): el
            for el
            in obj.driver.find_elements(self.by, self.selector)
            if el.is_displayed()
        }


class PageAdapter(object):

    """Page adapter base class."""

    def __init__(self, driver):
        """Stash context and driver for later use."""
        self.driver = driver

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
        if el.tag_name == 'text':
            el.clear()
        webdriver.ActionChains(
            self.driver,
        ).send_keys(text).perform()
        if el.tag_name in ('text', 'password'):
            assert el.get_attribute('value') == text, \
                '%r not set in %r' % (text, el)
