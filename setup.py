#!/usr/bin/env python
"""PageAdapter pattern for Python Selenium browser test abstraction."""
from setuptools import setup, find_packages

setup(
    name='selenium_page_adapter',
    version='0.2.0',
    description=__doc__,
    long_description=open('README.rst').read(),
    author='Tyson Clugg',
    author_email='tyson@clugg.net',
    url='https://selenium_page_adapter.readthedocs.org/en/latest/',
    license='MIT',
    packages=find_packages(),
    test_suite='selenium_page_adapter.tests',
    install_requires=[
        'selenium',
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
)
