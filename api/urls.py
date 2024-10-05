from django.urls import path

from .admin import get_group_configs, lock_group, SuspendConfig, VpsConfig
from .snapshot import VpsSnapshotAPI, restore_vsp
from .support import TicketCollectionAPI, TicketAPI, ticket_reply
from .account import AccountAPI, AccountBalanceAPI, UserTokenAPI, delete_token, AccountCollectionAPI
from .invoices import InvoiceCollectionAPI, InvoiceAPI
from .views import RegisterAPI, LoginAPI, LogoutAPI
from .vps.archived_vps import archived_vps
from .vps.change_pass import change_pass_vps
from .vps.create import create_vps
from .vps import VPSAPI, start_vps, stop_vps, restart_vps, suspend_vps, unsuspend_vps, give_vps, change_vps_plan, \
    update_info
from .vps.delete import delete_vps
from .vps.rebuild import rebuild_vps
from .vps.refund import refund_vps
from .vps_log import get_vps_logs
from .balances import topup, reclaim
from .vps.calculator import vps_calculator
from .payment import get_payment_url, paypal_success_callback, paypal_cancel_callback, paypal_webhook, \
    bank_webhook, generate_qr_code

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('vps/create', create_vps, name='create-vps'),
    path('vps/get_archived_vps', archived_vps, name='archived_vps'),
    path('vps/start/', start_vps, name='start-vps'),
    path('vps/stop/', stop_vps, name='stop-vps'),
    path('vps/restart/', restart_vps, name='restart-vps'),
    path('vps/delete/', delete_vps, name='delete-vps'),
    path('vps/rebuild/', rebuild_vps, name='rebuild-vps'),
    path('vps/suspend/', suspend_vps, name='suspend-vps'),
    path('vps/unsuspend/', unsuspend_vps, name='unsuspend-vps'),
    path('vps/change_pass/', change_pass_vps, name='change-pass-vps'),
    path('vps/give/', give_vps, name='give-vps'),
    path('vps/<str:vps_id>/change_plan', change_vps_plan, name='change_vps_plan'),
    path('vps/<str:vps_id>/refund/', refund_vps, name='refund_vps'),
    path('vps/<str:vps_id>/update_info/', update_info, name='update_info'),

    path('vps/calculator', vps_calculator, name='vps_calculator'),
    path('vps/logs/', get_vps_logs, name='get_vps_logs'),
    path('vps/', VPSAPI.as_view(), name='vps'),
    path('accounts/', AccountCollectionAPI.as_view(), name='account-collection'),
    path('account/profile/', AccountAPI.as_view(), name='user-profile'),
    path('account/balance/', AccountBalanceAPI.as_view(), name='user-balance'),
    path('account/balance/topup/', topup, name='user-balance-topup'),
    path('account/balance/reclaim/', reclaim, name='user-balance-reclaim'),

    path('payment/get_payment_url/', get_payment_url, name='get_payment_url'),
    path('payment/get_qr_code/', generate_qr_code, name='get_qr_code'),
    path('payment/paypal/success/', paypal_success_callback, name='paypal_success_callback'),
    path('payment/paypal/cancel/', paypal_cancel_callback, name='paypal_cancel_callback'),
    path('payment/paypal/webhook/', paypal_webhook, name='paypal_webhook'),
    path('payment/bank/webhook/', bank_webhook, name='bank_webhook'),

    path('invoice/', InvoiceCollectionAPI.as_view(), name='invoice'),
    path('invoices/', InvoiceCollectionAPI.as_view(), name='api-invoices'),
    path('invoices/<str:invoice_id>', InvoiceAPI.as_view(), name='api-invoice'),
    path('tickets/', TicketCollectionAPI.as_view(), name='tickets_view'),
    path('tickets/<str:ticket_id>/', TicketAPI.as_view(), name='ticket_view'),
    path('tickets/<str:ticket_id>/reply/', ticket_reply, name='ticket_reply'),

    path('tokens/', UserTokenAPI.as_view(), name='user-tokens'),
    path('tokens/<str:token_id>/', delete_token, name='delete-token'),

    path('snapshots/<str:vps_id>/', VpsSnapshotAPI.as_view(), name='vps-snapshots'),
    path('snapshots/<str:vps_id>/restore/', restore_vsp, name='vps-snapshots'),

    path('admin/group_config/', get_group_configs, name='group-config'),
    path('admin/group_config/lock', lock_group, name='lock_group'),
    path('admin/suspend_config/', SuspendConfig.as_view(), name='suspend-config'),
    path('admin/vps_config/', VpsConfig.as_view(), name='vps-config'),
]
