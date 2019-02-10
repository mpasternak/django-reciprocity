import time

from celery import task

from reciprocity.core import WebPage


@task
def long_running_task(web_page_uuid):
    w = WebPage(uuid=web_page_uuid)

    w.progress_dialog_init(
        "This will take some time",
        "Let's try to find coolest interactive web library for Django",
        "Search in progress...")
    time.sleep(2)

    for elem in range(1, 11):
        w.progress_dialog_update(elem * 10)
        time.sleep(1)

    w.progress_dialog_close()
    w.callout(
        header="The coolest interactive web library for Django has been found!",
        body="Will display its web page in 3 seconds...")
    time.sleep(3)
    w.gotoPage("http://github.com/mpasternak/django-reciprocity/")
