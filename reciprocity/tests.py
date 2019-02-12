from django.test import TestCase

from reciprocity import core
from reciprocity.core import ProgressDialogMixin, CalloutMixin, GotoPageMixin, SingleQueue, WebPage


class MockQueue:
    publishCalled = False

    def publish(self, *args, **kw):
        self.publishCalled = True


class TestReciprocity_Core_ProgressDialogMixin(TestCase):
    def setUp(self):
        class ProgressTest(MockQueue, ProgressDialogMixin):
            pass

        self.obj = ProgressTest()

    def test_progress_dialog_init(self):
        self.obj.progress_dialog_init("header", "lead", "para")
        self.assert_(self.obj.publishCalled)

    def test_progress_dialog_update(self):
        self.obj.progress_dialog_update("value")
        self.assert_(self.obj.publishCalled)

    def test_progress_dialog_close(self):
        self.obj.progress_dialog_close()
        self.assert_(self.obj.publishCalled)


class TestReciprocity_Core_CalloutPageMixin(TestCase):
    def setUp(self):
        class CalloutTest(MockQueue, CalloutMixin):
            pass

        self.obj = CalloutTest()

    def test_callout(self):
        self.obj.callout("header", "body")
        self.assert_(self.obj.publishCalled)


class TestReciprocity_Core_GotoPageMixin(TestCase):
    def setUp(self):
        class GotoPageTest(MockQueue, GotoPageMixin):
            pass

        self.obj = GotoPageTest()

    def test_gotoPage(self):
        self.obj.gotoPage("onet.pl")
        self.assert_(self.obj.publishCalled)


class TestReciprocity_Core_SingleQueue(TestCase):
    def setUp(self):
        self.called = False

    def publish_message(self, *args, **kw):
        self.called = True

    def test_publish(self):
        orig_publish_message = core.publish_message

        try:
            core.publish_message = self.publish_message
            sq = SingleQueue()
            sq.queue_type = "foo"
            sq.publish(foo="bar")
        finally:
            core.publish_message = orig_publish_message

        self.assert_(self.called)


class TestReciprocity_Core_WebPage(TestCase):
    def setUp(self):
        self.called = False

    def publish_message(self, *args, **kw):
        self.called = True

    def test_publish(self):
        orig_publish_message = core.publish_message

        try:
            core.publish_message = self.publish_message
            w = WebPage("uuid")
            w.publish(foo="bar")
        finally:
            core.publish_message = orig_publish_message

        self.assert_(self.called)
