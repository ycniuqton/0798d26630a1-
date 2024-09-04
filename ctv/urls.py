from django.urls import path
from .views import proxy_view


urlpatterns = [
    path('/(?P<proxy_path>.*)$', proxy_view, name='ctv_proxy'),
]
