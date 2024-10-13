from admin_datta.views import UserLoginView
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.views.generic import CreateView
from services.account import AccountRepository
from services.mail_service import VPSMailService


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


from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView


# Custom Registration Form
class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label=_("First Name"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=True  # Set required as per your need
    )
    last_name = forms.CharField(
        label=_("Last Name"),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=True
    )


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
        fields = ('username', 'email', 'first_name', 'last_name')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }

    # Overriding clean method to validate username, email, and other fields if needed
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")

        User = get_user_model()

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            self.add_error('username', ValidationError(_("This username is already taken.")))

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            self.add_error('email', ValidationError(_("This email is already registered.")))

        return cleaned_data


# User Registration View
class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')  # Using reverse_lazy for cleaner URL handling

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = get_user_model().objects.get(username=request.POST['username'])
            ar = AccountRepository()
            ar.create_account(user.id)
            VPSMailService().send_register_email(user)
        return response
