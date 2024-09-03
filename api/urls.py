from django.urls import path

from .support import TicketCollectionAPI, TicketAPI
from .account import AccountAPI, AccountBalanceAPI
from .invoices import InvoiceAPI
from .views import RegisterAPI, LoginAPI, LogoutAPI
from .vps.create import create_vps
from .vps import VPSAPI, start_vps, stop_vps, restart_vps, suspend_vps, unsuspend_vps, give_vps
from .vps_log import get_vps_logs
from .balances import topup
from .vps.calculator import vps_calculator

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('vps/create', create_vps, name='create-vps'),
    path('vps/start/', start_vps, name='start-vps'),
    path('vps/stop/', stop_vps, name='stop-vps'),
    path('vps/restart/', restart_vps, name='restart-vps'),
    path('vps/suspend/', suspend_vps, name='suspend-vps'),
    path('vps/unsuspend/', unsuspend_vps, name='unsuspend-vps'),
    path('vps/give/', give_vps, name='give-vps'),

    path('vps/calculator', vps_calculator, name='vps_calculator'),
    path('vps/logs/', get_vps_logs, name='get_vps_logs'),
    path('vps/', VPSAPI.as_view(), name='vps'),
    path('account/profile/', AccountAPI.as_view(), name='user-profile'),
    path('account/balance/', AccountBalanceAPI.as_view(), name='user-balance'),
    path('account/balance/topup', topup, name='user-balance'),
    path('invoice/', InvoiceAPI.as_view(), name='invoice'),
    path('tickets/', TicketCollectionAPI.as_view(), name='tickets_view'),
    path('tickets/<str:ticket_id>/', TicketAPI.as_view(), name='ticket_view'),
]
