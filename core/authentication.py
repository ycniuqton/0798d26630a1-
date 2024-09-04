from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework.authentication import BasicAuthentication, TokenAuthentication, BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.http import HttpResponseRedirect
from django.urls import reverse

from home.models import UserToken


class RedirectToLoginException(AuthenticationFailed):
    pass


class CookieBasicAuthentication(TokenAuthentication):
    keyword = ''

    def authenticate(self, request):
        # Retrieve token from the 'auth_token' cookie
        auth_token = request.COOKIES.get('basic_token')
        if not auth_token:
            login_url = reverse('login')  # Replace 'login' with the name of your login URL
            raise RedirectToLoginException(HttpResponseRedirect(login_url))

        # Call the parent's method to validate the token
        try:
            return self.authenticate_credentials(auth_token)
        except AuthenticationFailed:
            login_url = reverse('login')  # Replace 'login' with the name of your login URL
            raise RedirectToLoginException(HttpResponseRedirect(login_url))


class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if not request.path.startswith('/api/'):
            return None
        api_key = request.headers.get('X-API-KEY')  # Get the API key from request headers

        if not api_key:
            return None  # No API key provided, continue to next authentication class.

        user_token = UserToken.objects.filter(token=api_key).first()

        if not user_token:
            return None
        if user_token.expired_at < timezone.now() and user_token.ttl != -1:
            return None

        # Authentication successful, return the user associated with the API key
        return (user_token.user, None)
