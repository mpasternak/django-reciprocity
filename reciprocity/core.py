from nginx_push_stream.const import QUEUE_UUID, QUEUE_ALL_USERS, QUEUE_ALL_LOGGED
from nginx_push_stream.core import publish_message


class ProgressDialogMixin:
    def progress_dialog_init(self, header, lead, paragraph):
        return self.publish(type="progress-dialog-init", header=header, lead=lead, paragraph=paragraph)

    def progress_dialog_update(self, value):
        return self.publish(type="progress-dialog-update", value=value)

    def progress_dialog_close(self):
        return self.publish(type="progress-dialog-close")


class CalloutMixin:
    def callout(self, header, body, klass="success"):
        return self.publish(type="callout", header=header, body=body, **{"class": klass})


class GotoPageMixin:
    def gotoPage(self, href):
        return self.publish(type="goto-page", href=href)


class EveryMixin(ProgressDialogMixin, CalloutMixin, GotoPageMixin):
    pass


class SingleQueue:
    def publish(self, **message):
        return publish_message(self.queue_type, **message)


class AllUsers(SingleQueue, EveryMixin):
    queue_type = QUEUE_ALL_USERS


class AuthorisedUsers(SingleQueue, EveryMixin):
    queue_type = QUEUE_ALL_LOGGED


class WebPage(EveryMixin):
    queue_type = QUEUE_UUID

    def __init__(self, uuid):
        self.uuid = uuid

    def publish(self, **message):
        return publish_message(self.queue_type + self.uuid, **message)
