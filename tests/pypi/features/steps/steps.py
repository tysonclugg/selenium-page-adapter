"""Step implementations for PyPi BDD test suite."""

from behave import given, when, then


def package_url(package_name):
    """Return PyPi package URL for given package name."""
    return 'https://pypi.python.org/pypi/%s/' % package_name


@given(u"I'm on the home page")
def im_on_the_home_page(context):
    """Visit the PyPi home page."""
    context.pypi.go_home()


@when(u'I search for "{query}"')
def i_search_for_query(context, query):
    """Search PyPi packages matching query string."""
    context.pypi.search(query)


@then(u'"{package}" appears in the search results.')
def package_appears_in_the_search_results(context, package):
    """Assert that the named package appears in current PyPi search results."""
    package_url_fragment = package_url(package)
    result_urls = [
        result.url
        for result
        in context.pypi.search_results.values()
    ]
    assert any(
        result_url.startswith(package_url_fragment)
        for result_url
        in result_urls
    ), result_urls


@then(u'I am shown the "{package}" page.')
def i_am_shown_the_package_page(context, package):
    """Assert that we are on the URL for the named package."""
    package_url_fragment = package_url(package)
    assert (
        context.driver.current_url.startswith(package_url_fragment)
    ), context.driver.current_url


@then(u'no results appear.')
def no_results_appear(context):
    """Assert that no results appear in the PyPi search results."""
    assert len(context.pypi.search_results) == 0
