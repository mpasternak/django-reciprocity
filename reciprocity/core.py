from nginx_push_stream.const import QUEUE_UUID, QUEUE_ALL_USERS, QUEUE_ALL_LOGGED
from nginx_push_stream.core import publish_message


class CalloutMixin:
    def callout(self, header, body, klass="success"):
        return self.publish(type="callout", header=header, body=body, **{"class": klass})


class GotoPageMixin:
    def gotoPage(self, href):
        return self.publish(type="goto-page", href=href)


class ModalDialogMixin:
    def modalDialog(self, paragraph, lead=None, header=None):
        return self.publish(type="modal-dialog", paragraph=paragraph, lead=lead, header=header)

    def closeModalDialog(self):
        return self.publish(type="close-modal-dialog")


class PleaseWaitDialogMixin:
    def pleaseWaitDialog(self, paragraph, lead=None, header=None):
        return self.publish(type="please-wait-dialog", paragraph=paragraph, lead=lead, header=header)

    def closePleaseWaitDialog(self):
        return self.publish(type="close-please-wait-dialog")


class ProgressDialogMixin:
    def progressDialogInit(self, paragraph, lead=None, header=None):
        return self.publish(type="progress-dialog-init",
                            header=header, lead=lead, paragraph=paragraph)

    def progressDialogUpdate(self, value):
        return self.publish(type="progress-dialog-update",
                            value=value)

    def progressDialogClose(self):
        return self.publish(type="progress-dialog-close")

class EveryMixin(ProgressDialogMixin, CalloutMixin, GotoPageMixin, ModalDialogMixin,
                 PleaseWaitDialogMixin):
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
