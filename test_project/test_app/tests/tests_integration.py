import time

import pytest
from django.conf import settings
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import visibility_of_element_located, \
    invisibility_of_element_located, text_to_be_present_in_element
from selenium.webdriver.support.wait import WebDriverWait

from reciprocity.core import WebPage
from .selenium_utils import page_source_contains, wait_timeout

TEXT_BEFORE_UUID = "My web page ID is: "
TEXT_CALLOUT_HEADER = "This was added dynamically via NGINX-Http-Push-Stream"


@pytest.fixture
def uuid(selenium, live_server):
    selenium.get("http://webserver/")
    WebDriverWait(selenium, wait_timeout).until(page_source_contains(TEXT_BEFORE_UUID))
    uuid = selenium.page_source.split("My web page ID is: ")[1].split(".")[0]

    if selenium.find_element_by_id("jquery-loading-error").is_displayed():
        raise Exception("jQuery did not load. Did you ran 'yarn --dev' in 'test_project'?")

    return uuid


def test_integration_callout(uuid, selenium):
    WebPage(uuid).callout(TEXT_CALLOUT_HEADER, "body")

    try:
        WebDriverWait(selenium, wait_timeout).until(page_source_contains(TEXT_CALLOUT_HEADER))
    except TimeoutException:
        if selenium.page_source.find("Cannot connect to notification server"):
            raise Exception("Cannot connect to notification server via selenium: %s %s" % (
                settings.NGINX_PUSH_STREAM_SUB_HOST,
                settings.NGINX_PUSH_STREAM_SUB_PORT,
            ))


@pytest.mark.urls('test_project.test_urlpatterns')
def test_integration_gotoPage(uuid, selenium):
    WebPage(uuid).gotoPage("http://webserver/testGoto")
    WebDriverWait(selenium, wait_timeout).until(page_source_contains("gotoPage works"))


def test_integration_modalDialog(uuid, selenium):
    wp = WebPage(uuid)

    wp.modalDialog("Modal dialog text")

    WebDriverWait(selenium, wait_timeout).until(
        visibility_of_element_located((By.ID, "reciprocity-modal-dialog"))
    )

    wp.closeModalDialog()

    WebDriverWait(selenium, wait_timeout).until(
        invisibility_of_element_located((By.ID, "reciprocity-modal-dialog"))
    )


def test_integration_pleaseWaitDialog(uuid, selenium):
    wp = WebPage(uuid)

    wp.pleaseWaitDialog("Modal dialog text")

    WebDriverWait(selenium, wait_timeout).until(
        visibility_of_element_located((By.ID, "reciprocity-please-wait-dialog"))
    )

    wp.closePleaseWaitDialog()

    WebDriverWait(selenium, wait_timeout).until(
        invisibility_of_element_located((By.ID, "reciprocity-please-wait-dialog"))
    )



def test_integration_progressDialog(uuid, selenium):
    wp = WebPage(uuid)

    wp.progressDialogInit("Modal dialog text")

    WebDriverWait(selenium, wait_timeout).until(
        visibility_of_element_located((By.ID, "reciprocity-progress-dialog"))
    )

    wp.progressDialogUpdate(99)

    WebDriverWait(selenium, wait_timeout).until(
        text_to_be_present_in_element((By.ID, "reciprocity-progress-meter"), "99%")
    )

    wp.progressDialogClose()

    WebDriverWait(selenium, wait_timeout).until(
        invisibility_of_element_located((By.ID, "reciprocity-please-wait-dialog"))
    )

