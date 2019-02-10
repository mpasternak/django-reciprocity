from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.generic import TemplateView

from .tasks import long_running_task


class RootPage(TemplateView):
    template_name = "root.html"


def start_long_process(request):
    if not request.is_ajax():
        return HttpResponseNotAllowed()
    long_running_task.delay(web_page_uuid=request.GET['uuid'])
    return HttpResponse("{}")
