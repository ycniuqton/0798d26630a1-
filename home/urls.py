from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
  path('tables/', views.tables, name='tables'),


  path('instances/', views.instances, name='instances'),
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
  path('affiliate/', views.affiliate, name='affiliate'),
  path('account/', views.account, name='account'),
]
