from django.urls import path

from .account import AccountAPI, AccountBalanceAPI
from .views import RegisterAPI, LoginAPI, LogoutAPI
from .vps.create import create_vps
from .vps import VPSAPI
from .vps_log import get_vps_logs
from .balances import topup

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('vps/create', create_vps, name='create-vps'),
    path('vps/logs/', get_vps_logs, name='get_vps_logs'),
    path('vps/', VPSAPI.as_view(), name='vps'),
    path('account/profile/', AccountAPI.as_view(), name='user-profile'),
    path('account/balance/', AccountBalanceAPI.as_view(), name='user-balance'),
    path('account/balance/topup', topup, name='user-balance'),
]
