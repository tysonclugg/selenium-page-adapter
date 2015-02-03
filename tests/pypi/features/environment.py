"""DuckDuckGo BDD environment."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_page_adapter import PageAdapter, ElementDescriptor, \
    AvailableElements, AllElements


class SearchResult(PageAdapter):
    result_link = ElementDescriptor(By.CSS_SELECTOR, 'td:nth-of-type(1) a')
    result_weight = ElementDescriptor(By.CSS_SELECTOR, 'td:nth-of-type(2)')
    result_description = ElementDescriptor(By.CSS_SELECTOR, 'td:nth-of-type(3)')

    @property
    def title(self):
        return self.result_link.text.strip()

    @property
    def url(self):
        return self.result_link.get_attribute('href')

    @property
    def weight(self):
        return int(self.result_weight.text)

    @property
    def description(self):
        return self.result_description.text.strip()


class PyPiAdapter(PageAdapter):
    search_input = ElementDescriptor(By.ID, 'term')
    search_submit = ElementDescriptor(By.ID, 'submit')

    search_results = AvailableElements(
        lambda el: el.find_element(By.CSS_SELECTOR, 'a').text,
        By.CSS_SELECTOR, '.list tr[class]',
        wrapper=SearchResult,
    )

    def go_home(self):
        self.driver.get('https://pypi.python.org/pypi')

    def search(self, query):
        self.fill(self.search_input, query)
        self.search_submit.click()


def before_all(context):
    context.driver = webdriver.Firefox()
    context.pypi = PyPiAdapter(context.driver)

def after_all(context):
    """Tear down hospital BDD test context."""
    context.driver.quit()


def after_scenario(context, scenario):
    """Clean up after every test scenario."""
    context.driver.delete_all_cookies()
