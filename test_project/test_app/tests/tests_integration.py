from django.conf import settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from reciprocity.core import WebPage
from test_project.settings_pytest import NGINX_PUSH_STREAM_PUB_HOST
from .selenium_utils import page_source_contains, wait_timeout


TEXT_BEFORE_UUID = "My web page ID is: "
TEXT_CALLOUT_HEADER = "This was added dynamically via NGINX-Http-Push-Stream"


def test_integration_callout(selenium, live_server):
    selenium.get("http://webserver/")
    WebDriverWait(selenium, wait_timeout).until(page_source_contains(TEXT_BEFORE_UUID))

    uuid = selenium.page_source.split("My web page ID is: ")[1].split(".")[0]

    WebPage(uuid).callout(TEXT_CALLOUT_HEADER, "body")

    try:
        WebDriverWait(selenium, wait_timeout).until(page_source_contains(TEXT_CALLOUT_HEADER))
    except TimeoutException:
        if selenium.page_source.find("Cannot connect to notification server"):
            raise Exception("Cannot connect to notification server via selenium: %s %s" % (
                settings.NGINX_PUSH_STREAM_SUB_HOST,
                settings.NGINX_PUSH_STREAM_SUB_PORT,
            ))
