from django.urls import path
from django.contrib.auth import views as auth_views

from home import views
from .views import manage_tokens, delete_token, set_introducer, \
    current_introducer, tickets_view, faqs_view
from home.views.instances import instances, create_instances, instance_detail
from home.views.statics import FlagAPI, OSIconAPI
from home.views.accounts import *
from home.views.financial import invoices_view, financial_view, payment_view, billing_view, resource_record

urlpatterns = [
    path('', views.index, name='index'),
    path('tables/', views.tables, name='tables'),

    path('home/', views.home, name='home'),

    path('instances/', instances, name='instances'),
    path('instances/create/', create_instances, name='create_instances'),
    path('instance/<str:instance_id>/', instance_detail, name='instance_detail'),

    path('accounts/login/', CustomUserLoginView.as_view(), name='login'),
    path('accounts/register/', UserRegistrationView.as_view(), name='register'),
    path('accounts/logout/', logout_view, name='logout'),

    path('network/', views.network, name='network'),
    path('block_storage/', views.block_storage, name='block_storage'),
    path('snapshot/', views.snapshot, name='snapshot'),
    path('firewall/', views.firewall, name='firewall'),
    path('image/', views.image, name='image'),
    path('monitoring/', views.monitoring, name='monitoring'),

    path('payment/', payment_view, name='payment'),
    path('billing/', billing_view, name='billing'),
    path('resource_record/', resource_record, name='resource_record'),

    path('financial/', financial_view, name='financial'),
    path('support/', views.support, name='support'),
    path('ticket/', views.ticket, name='ticket'),
    path('your_tickets/', views.your_tickets, name='your_tickets'),
    path('api/your_tickets/', views.api_your_tickets, name='api_your_tickets'),
    path('api/tickets/', tickets_view, name='tickets_view'),
    path('api/your_tickets/<str:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('affiliate/', views.affiliate, name='affiliate'),
    path('your_introducer/', views.your_introducer, name='your_introducer'),
    path('link_code/', views.link_code, name='link_code'),
    path('affiliate_stats/', views.affiliate_stats, name='affiliate_stats'),
    path('account/', views.account, name='account'),
    path('profile/', views.profile, name='profile'),
    path('authentication/', views.authentication, name='authentication'),
    path('notifications/', views.notifications, name='notifications'),

    path('api/tokens/', manage_tokens, name='manage-tokens'),
    path('api/tokens/<str:token_id>/', delete_token, name='delete-token'),
    path('api/set-introducer/', set_introducer, name='set_introducer'),
    path('api/current-introducer/', current_introducer, name='current_introducer'),
    path('api/faqs/', faqs_view, name='faqs_view'),
    path('invoices/', invoices_view, name='invoices'),
    path('api/vps/<int:instance_id>/vnc-link/', views.get_vnc_link, name='get_vnc_link'),
    path('api/vps/<int:instance_id>/snapshots/', views.get_snapshots, name='get_snapshots'),
    path('api/vps/history/', views.vps_history, name='vps_history'),

    path('api/static/flags/<str:country_code>/', FlagAPI.as_view(), name='country_flag_api'),
    path('api/static/os_icon/<str:os_code>/', OSIconAPI.as_view(), name='os_icon_api'),
]
