import contextlib

from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support.wait import WebDriverWait

wait_timeout = 10


class page_source_contains(object):
    """ Wait until page source contains text.
    """

    def __init__(self, text):
        self.text = text

    def __call__(self, browser):
        if browser.page_source.find(self.text) >= 0:
            return True
        return False


@contextlib.contextmanager
def wait_for_page_load(self, timeout=wait_timeout):
    old_page = self.find_element_by_tag_name('html')
    yield WebDriverWait(self, timeout).until(staleness_of(old_page))
