# myapp/exception_handlers.py

from rest_framework.views import exception_handler
from django.http import HttpResponseRedirect
from django.urls import reverse
from core.authentication import RedirectToLoginException


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the additional logic for RedirectToLoginException
    if isinstance(exc, RedirectToLoginException):
        # Redirect to the login page
        login_url = reverse('login')  # Adjust this URL name accordingly
        return HttpResponseRedirect(login_url)

    return response
