from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from .models import *

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)


def instances(request):
  context = {
    'segment': 'instances'
  }
  return render(request, "pages/instances.html", context)


def create_instances(request):
  context = {
    'segment': 'create_instances'
  }
  return render(request, "pages/create-instances.html", context)



def network(request):
  context = {
    'segment': 'network'
  }
  return render(request, "pages/dynamic-tables.html", context)


def block_storage(request):
  context = {
    'segment': 'block_storage'
  }
  return render(request, "pages/dynamic-tables.html", context)



def snapshot(request):
  context = {
    'segment': 'snapshot'
  }
  return render(request, "pages/dynamic-tables.html", context)



def firewall(request):
  context = {
    'segment': 'firewall'
  }
  return render(request, "pages/dynamic-tables.html", context)



def image(request):
  context = {
    'segment': 'image'
  }
  return render(request, "pages/dynamic-tables.html", context)



def monitoring(request):
  context = {
    'segment': 'monitoring'
  }
  return render(request, "pages/dynamic-tables.html", context)


def payment(request):
  context = {
    'segment': 'payment'
  }
  return render(request, "pages/dynamic-tables.html", context)



def resource_record(request):
  context = {
    'segment': 'resource_record'
  }
  return render(request, "pages/dynamic-tables.html", context)



def billing(request):
  context = {
    'segment': 'billing'
  }
  return render(request, "pages/dynamic-tables.html", context)





def financial(request):
  context = {
    'segment': 'financial'
  }
  return render(request, "pages/dynamic-tables.html", context)



def support(request):
  context = {
    'segment': 'support'
  }
  return render(request, "pages/dynamic-tables.html", context)



def affiliate(request):
  context = {
    'segment': 'affiliate'
  }
  return render(request, "pages/dynamic-tables.html", context)



def account(request):
  context = {
    'segment': 'account'
  }
  return render(request, "pages/dynamic-tables.html", context)
