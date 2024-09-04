from admin_datta.views import UserLoginView, UserRegistrationView
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django import forms
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from services.account import AccountRepository


class CustomUserLoginView(UserLoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            token, created = Token.objects.get_or_create(user=request.user)
            expired = datetime.utcnow() + timedelta(days=7)
            expired = expired.strftime("%A %B %D %Y %I:%M:%S")
            response.headers[
                'set-cookie'] = f'basic_token={token.key}; expires={expired}; Max-Age=31449600; Path=/; SameSite=Lax'
        except:
            pass
        return response


def logout_view(request):
    # Create a response object
    response = redirect('/accounts/login/')

    # Clear the 'basic_token' cookie
    response.delete_cookie('basic_token')

    return response


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            })
        }


class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = RegistrationForm
    success_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = get_user_model().objects.get(username=request.POST['username'])
        ar = AccountRepository()
        ar.create_account(user.id)
        return response
