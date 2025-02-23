from admin_datta.views import UserLoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from datetime import datetime, timedelta
from django.views.generic import CreateView
from django.views import View
from django.contrib.auth import get_user_model, login, logout
from django.conf import settings
from google.oauth2 import id_token
from google.auth.transport import requests
from django.http import JsonResponse
import json
import logging
from django.core.cache import cache
from django.utils import timezone
import time

logger = logging.getLogger(__name__)

from core import settings
from services.account import AccountRepository
from services.mail_service import VPSMailService
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
import os
import secrets
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.hashers import make_password
from home.models import PendingRegistration


class CustomUserLoginView(UserLoginView):
    def form_invalid(self, form):
        """Handle invalid login attempts"""
        # Get client IP for rate limiting
        client_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR'))
        cache_key = f'login_attempts_ip_{client_ip}'
        attempt_count = cache.get(cache_key, 0)

        # Increment and store attempt count
        cache.set(cache_key, attempt_count + 1, 3600)  # 1 hour expiry

        if attempt_count >= 5:  # Max 5 attempts per hour
            messages.warning(
                self.request,
                'Too many login attempts. Please try again later.'
            )
            # Add a delay to prevent brute force attacks
            time.sleep(2)
        else:
            # Generic error message that doesn't reveal if username exists
            messages.warning(
                self.request,
                'Invalid username or password.'
            )
            
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            
            if request.user.is_authenticated:
                # Only set token if login was successful
                token, created = Token.objects.get_or_create(user=request.user)
                expired = datetime.utcnow() + timedelta(days=7)
                expired = expired.strftime("%A %B %D %Y %I:%M:%S")
                response.headers[
                    'set-cookie'] = f'basic_token={token.key}; expires={expired}; Max-Age=31449600; Path=/; SameSite=Lax'
            
            return response
            
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            messages.error(request, 'An error occurred. Please try again.')
            return self.form_invalid(self.get_form())


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
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']

            # Check if email or username already exists in User model
            User = get_user_model()
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'This email is already registered.')
                return self.form_invalid(form)

            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
                return self.form_invalid(form)

            # Check for existing pending registration
            existing_pending = PendingRegistration.objects.filter(
                email=email,
                is_confirmed=False
            ).first()

            if existing_pending:
                # If expired, delete it and create new one
                if existing_pending.is_expired():
                    existing_pending.delete()
                else:
                    # If not expired, send error message
                    messages.info(
                        self.request,
                        'A confirmation email was already sent. Please check your inbox or wait for the current registration to expire.'
                    )
                    return render(self.request, 'accounts/registration-confirmation.html', {
                        'email': email
                    })

            # Create pending registration instead of user
            pending = PendingRegistration.objects.create(
                email=email,
                username=username,
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                password=make_password(form.cleaned_data['password1'])
            )

            # Generate confirmation URL
            confirmation_url = self.request.build_absolute_uri(
                f'/accounts/confirm/{pending.confirmation_token}'
            )
            print(confirmation_url)
            # Send confirmation email
            mail_service = VPSMailService()
            mail_service.send_confirmation_email(
                email=pending.email,
                username=pending.username,
                confirmation_url=confirmation_url,
                expires_at=pending.expires_at
            )

            # Render confirmation page instead of redirecting to login
            return render(self.request, 'accounts/registration-confirmation.html', {
                'email': email
            })

        except Exception as e:
            print(f"Registration error: {str(e)}")  # For debugging
            messages.error(
                self.request,
                'An error occurred during registration. Please try again.'
            )
            return super().form_invalid(form)


class ConfirmRegistrationView(View):
    def get(self, request, token):
        try:
            pending = PendingRegistration.objects.get(
                confirmation_token=token,
                is_confirmed=False
            )

            # Check if registration is blocked due to too many failed attempts
            if pending.is_blocked():
                messages.error(request, 'This registration is temporarily blocked due to too many failed attempts. Please try again later.')
                return redirect('register')

            if pending.is_expired():
                messages.warning(request, 'The confirmation link has expired. Please register again.')
                pending.delete()
                return redirect('register')

            # Create the actual user
            User = get_user_model()
            user = User.objects.create(
                username=pending.username,
                email=pending.email,
                first_name=pending.first_name,
                last_name=pending.last_name,
                password=pending.password  # Already hashed
            )

            # Set up the new user account
            ar = AccountRepository()
            ar.setup_new_user(user)

            # Mark registration as confirmed and save
            pending.is_confirmed = True
            pending.save()

            # Instead of redirecting to login, show success page
            return render(request, 'accounts/registration-success.html')

        except PendingRegistration.DoesNotExist:
            # Track failed attempt by IP
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            cache_key = f'confirm_attempts_ip_{client_ip}'
            attempt_count = cache.get(cache_key, 0)
            
            if attempt_count >= 10:  # Max 10 failed attempts per IP per hour
                messages.error(request, 'Too many failed attempts. Please try again later.')
                return redirect('register')
                
            cache.set(cache_key, attempt_count + 1, 3600)  # 1 hour expiry
            
            messages.warning(request, 'Invalid or expired confirmation link.')
            return redirect('register')
            
        except Exception as e:
            logger.error(f"Confirmation error: {str(e)}")
            messages.error(request, 'An error occurred while confirming your registration.')
            return redirect('register')


class ResendConfirmationView(View):
    def post(self, request):
        try:
            email = request.POST.get('email')
            if not email:
                return JsonResponse({'error': 'Email is required'}, status=400)

            # Get client IP for rate limiting
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            
            # Check IP-based rate limit (using cache)
            cache_key = f'email_resend_ip_{client_ip}'
            resend_count = cache.get(cache_key, 0)
            
            if resend_count >= 10:  # Max 10 resends per IP per hour
                return JsonResponse({
                    'error': 'Too many resend attempts. Please try again later.'
                }, status=429)

            pending = PendingRegistration.objects.filter(
                email=email,
                is_confirmed=False
            ).first()

            if not pending:
                return JsonResponse({
                    'error': 'No pending registration found for this email'
                }, status=404)

            if pending.is_expired():
                pending.delete()
                return JsonResponse({
                    'error': 'Registration has expired. Please register again.'
                }, status=400)

            # Check registration-specific rate limits
            if not pending.can_resend_email():
                return JsonResponse({
                    'error': 'Please wait before requesting another confirmation email.'
                }, status=429)

            # Generate new confirmation URL
            confirmation_url = request.build_absolute_uri(
                f'/accounts/confirm/{pending.confirmation_token}'
            )

            # Update rate limiting counters
            pending.resend_count += 1
            pending.last_resend_at = timezone.now()
            pending.save()

            # Update IP-based rate limit
            cache.set(cache_key, resend_count + 1, 3600)  # 1 hour expiry

            # Resend confirmation email
            mail_service = VPSMailService()
            mail_service.send_confirmation_email(
                email=pending.email,
                username=pending.username,
                confirmation_url=confirmation_url,
                expires_at=pending.expires_at
            )

            return JsonResponse({
                'message': 'Confirmation email has been resent'
            })

        except Exception as e:
            logger.error(f"Resend confirmation error: {str(e)}")
            return JsonResponse({
                'error': 'Failed to resend confirmation email'
            }, status=500)


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

            # Use the configured redirect URI
            flow.redirect_uri = settings.GoogleOAuthConfig.REDIRECT_URI

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
