from django.contrib import admin
from django.urls import path
from nginx_push_stream.auth import auth_request

from test_app.views import RootPage, start_long_process

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', auth_request),
    path('start', start_long_process, name="startLongProcess"),
    path('', RootPage.as_view())
]
