from django.shortcuts import render
from django.views.generic import TemplateView


class RootPage(TemplateView):
    template_name = "root.html"
    pass

