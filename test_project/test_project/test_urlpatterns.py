from django.urls import path

from test_app.views import test_gotoPage
from .urls import urlpatterns

urlpatterns = urlpatterns + [
    path('testGoto', test_gotoPage)
]
