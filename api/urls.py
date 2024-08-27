from django.urls import path
from .views import RegisterAPI, LoginAPI, LogoutAPI
from .vps.create import create_vps
from .vps_log import get_vps_logs

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('vps/create', create_vps, name='create-vps'),
    path('vps/logs/', get_vps_logs, name='get_vps_logs'),
]
