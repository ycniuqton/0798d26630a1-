from admin_datta.views import UserLoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import get_user_model, login
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse
import json
import logging

logger = logging.getLogger(__name__)

from core import settings
from services.account import AccountRepository
from services.mail_service import VPSMailService
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os
import secrets


@method_decorator(csrf_exempt, name='dispatch')
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
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationView(CreateView):
    template_name = 'accounts/auth-signup.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')  # Using reverse_lazy for cleaner URL handling

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 302:
            user = get_user_model().objects.get(username=request.POST['username'])
            ar = AccountRepository()
            ar.setup_new_user(user)
        return response


class OAuth2CallbackView(View):
    def get(self, request):
        try:
            # Get the flow from session
            flow = Flow.from_client_secrets_file(
                settings.GoogleOAuthConfig.CLIENT_SECRETS_FILE,
                scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                        'https://www.googleapis.com/auth/userinfo.profile'],
                state=request.GET.get('state')
            )
            flow.redirect_uri = request.build_absolute_uri('/oauth2/callback')

            # Exchange code for tokens
            flow.fetch_token(
                authorization_response=request.build_absolute_uri(),
                code=request.GET.get('code')
            )

            # Get credentials and user info
            credentials = flow.credentials
            session = flow.authorized_session()
            user_info = session.get('https://www.googleapis.com/oauth2/v2/userinfo').json()

            # Get or create user
            User = get_user_model()
            ar = AccountRepository()
            
            try:
                user = User.objects.get(email=user_info['email'])
            except User.DoesNotExist:
                # Create new user with OAuth data
                user = ar.create_user_from_oauth(
                    email=user_info['email'],
                    first_name=user_info.get('given_name', ''),
                    last_name=user_info.get('family_name', '')
                )

            # Store email in session for future logins
            request.session['last_google_email'] = user_info['email']
            
            # Login user
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            # Create auth token
            token, _ = Token.objects.get_or_create(user=user)

            # Set cookie and redirect
            response = redirect('/')
            expired = datetime.utcnow() + timedelta(days=7)
            expired_str = expired.strftime("%A %B %D %Y %I:%M:%S")
            response.set_cookie(
                'basic_token',
                token.key,
                expires=expired_str,
                max_age=31449600,
                path='/',
                samesite='Lax'
            )

            return response

        except Exception as e:
            logger.error(f"OAuth2 callback error: {str(e)}")
            return redirect('/accounts/login/?error=Authentication failed')


@method_decorator(csrf_exempt, name='dispatch')
class GoogleOAuth2InitView(View):
    def get(self, request):
        try:
            flow = Flow.from_client_secrets_file(
                settings.GoogleOAuthConfig.CLIENT_SECRETS_FILE,
                scopes=['openid', 'https://www.googleapis.com/auth/userinfo.email',
                        'https://www.googleapis.com/auth/userinfo.profile'],
                state=secrets.token_urlsafe(16)
            )
            flow.redirect_uri = request.build_absolute_uri('/oauth2/callback')

            auth_params = {
                'access_type': 'offline',
                'include_granted_scopes': 'true',
            }

            # Check if this is a returning user
            if 'last_google_email' in request.session:
                # For returning users, suggest their last used account but don't force it
                auth_params['login_hint'] = request.session['last_google_email']
            else:
                # For new users, show the consent screen and account selector
                auth_params['prompt'] = 'consent select_account'

            authorization_url, _ = flow.authorization_url(**auth_params)
            return redirect(authorization_url)

        except Exception as e:
            logger.error(f"OAuth2 init error: {str(e)}")
            return redirect('/accounts/login/?error=Failed to initialize authentication')
