"""Selenium Page Adapter."""
from collections import OrderedDict
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def maybe_wrapped(wrapper, driver, el):
    """Optionally wrap el with wrapper."""
    if wrapper is None:
        return el
    else:
        return wrapper(driver=driver, el=el)


class ElementDescriptor(object):

    """Data descriptor to ease getting specified element when required."""

    def __init__(self, by, selector, wrapper=None, el=None):
        """Stash our function to find element by selector args."""
        self.by = by
        self.selector = selector
        self.wrapper = wrapper
        #self.el = el

    def __get__(self, obj, cls=None):
        """Return our element if displayed."""
        # wait for element to exist
        parent = obj.el
        el = WebDriverWait(parent, 5).until(
            method=lambda root: root.find_element(self.by, self.selector),
            message='Element with %r = %r not found.' % (
                self.by,
                self.selector,
            ),
        )
        # now it exists, wait for it to become visible as per the W3C spec:
        # http://www.w3.org/TR/webdriver/#determining-visibility
        WebDriverWait(el, 5).until(
            method=lambda result: result.is_displayed(),
            message='Element with %r = %r is not displayed.' % (
                self.by,
                self.selector,
            ),
        )
        # element is now visible somewhere on the page, move mouse over it.
        webdriver.ActionChains(obj.driver).move_to_element(el)
        return maybe_wrapped(wrapper=self.wrapper, driver=obj.driver, el=el)


class AllElements(object):

    """Data descriptor to ease getting elements as dict."""

    filters = []

    def __init__(self, el_to_key, by, selector, wrapper=None, el=None):
        """Stash our function to generate keys and by selector args."""
        self.el_to_key = el_to_key
        self.by = by
        self.selector = selector
        self.wrapper = wrapper
        self.el = el

    def __get__(self, obj, cls=None):
        """Generate dict of items."""
        return OrderedDict(
            (
                self.el_to_key(el),
                maybe_wrapped(wrapper=self.wrapper, driver=obj.driver, el=el),
            )
            for el
            in obj.el.find_elements(self.by, self.selector)
            if not any(fltr(el) for fltr in self.filters)
        )


class AvailableElements(AllElements):

    """Data descriptor to ease getting available elements as dict."""

    filters = AllElements.filters + [
        (lambda el: not el.is_displayed()),
    ]
