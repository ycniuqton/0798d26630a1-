from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import vps_calculator, create_vps, user_profile, manage_tokens, delete_token, set_introducer, \
  current_introducer, tickets_view, faqs_view

urlpatterns = [
  path(''       , views.index,  name='index'),
  path('tables/', views.tables, name='tables'),

  path('home/', views.home, name='home'),

  path('instances/', views.instances, name='instances'),
  path('instance/<int:instance_id>/', views.instance_detail, name='instance_detail'),

  path('create_instances/', views.create_instances, name='create_instances'),

  path('network/', views.network, name='network'),
  path('block_storage/', views.block_storage, name='block_storage'),
  path('snapshot/', views.snapshot, name='snapshot'),
  path('firewall/', views.firewall, name='firewall'),
  path('image/', views.image, name='image'),
  path('monitoring/', views.monitoring, name='monitoring'),

  path('payment/', views.payment, name='payment'),
  path('billing/', views.billing, name='billing'),
  path('resource_record/', views.resource_record, name='resource_record'),
  # path('/', views., name=''),


  path('financial/', views.financial, name='financial'),
  path('support/', views.support, name='support'),
  path('ticket/', views.ticket, name='ticket'),
  path('affiliate/', views.affiliate, name='affiliate'),
  path('your_introducer/', views.your_introducer, name='your_introducer'),
  path('link_code/', views.link_code, name='link_code'),
  path('affiliate_stats/', views.affiliate_stats, name='affiliate_stats'),
  path('account/', views.account, name='account'),
  path('profile/', views.profile, name='profile'),
  path('authentication/', views.authentication, name='authentication'),
  path('notifications/', views.notifications, name='notifications'),
  path('api/vps-calculator/', vps_calculator, name='vps-calculator'),
  path('vps/create/', create_vps, name='create-vps'),
  path('api/user/profile/', user_profile, name='user-profile'),
  path('api/tokens/', manage_tokens, name='manage-tokens'),
  path('api/tokens/<str:token_id>/', delete_token, name='delete-token'),
  path('api/set-introducer/', set_introducer, name='set_introducer'),
  path('api/current-introducer/', current_introducer, name='current_introducer'),
  path('api/tickets/', tickets_view, name='tickets_view'),
  path('api/faqs/', faqs_view, name='faqs_view'),
  path('invoices/', views.invoices_view, name='invoices'),
]
