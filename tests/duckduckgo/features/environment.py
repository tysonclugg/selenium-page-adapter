"""DuckDuckGo BDD environment."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_page_adapter import PageAdapter, ElementDescriptor, \
    AvailableElements, AllElements


class Result(PageAdapter):
    result_title = ElementDescriptor(By.CLASS_NAME, 'result__title')
    result_url = ElementDescriptor(By.CLASS_NAME, 'result__url')

    @property
    def title(self):
        return self.result_title.text

    @property
    def url(self):
        return self.result_url.get_attribute('href')


class HomeAdapter(PageAdapter):
    search_input = ElementDescriptor(By.ID, 'search_form_input_homepage')
    search_reset = ElementDescriptor(By.ID, 'search_form_input_clear')
    search_submit = ElementDescriptor(By.ID, 'search_button_homepage')
    search_suggestions = AvailableElements(
        lambda el: (
            int(el.get_attribute('data-index')),
            el.text,
        ),
        By.CLASS_NAME,
        'acp',
    )

    results = AvailableElements(
        lambda el: el.id,
        By.CSS_SELECTOR, '.results, .results_links_deep, .highlight_d',
        wrapper=Result,
    )

    def go(self):
        self.driver.get('https://duckduckgo.com/')

    def search(self, query):
        self.fill(self.search_input, query)
        self.search_submit.click()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '.results, .results_links_deep'),
            ),
            self.page_source,
        )


def before_all(context):
    context.driver = webdriver.Firefox()
    context.home = HomeAdapter(context.driver)

def after_all(context):
    """Tear down hospital BDD test context."""
    context.driver.quit()


def after_scenario(context, scenario):
    """Clean up after every test scenario."""
    context.driver.delete_all_cookies()
