from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.http import HttpResponseRedirect
from django.urls import reverse


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
