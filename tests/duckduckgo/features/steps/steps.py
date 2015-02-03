from behave import given, when, then

@given(u"I'm on the home page")
def step_impl(context):
    context.home.go()

@when(u'I search for "{query}"')
def step_impl(context, query):
    context.home.search(query)

@then(u'the selenium_page_adapter PyPi page appears in the search results.')
def step_impl(context):
    pypi_url = u'https://pypi.python.org/pypi/selenium_page_adapter/'
    top_hits = [
        result.url
        for result
        in context.home.results.values()
    ]
    assert top_hits[0].startswith(pypi_url), 'Top hit mis-match: %s' % (top_hits[0])
    #assert pypi_url in top_hits, '%r\n%r\n%r' % (
    #    context.home.results,
    #    top_hits,
    #    context.home.page_source,
    #)
