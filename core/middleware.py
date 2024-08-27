# myapp/middleware.py

from django.http import HttpResponseRedirect
from core.authentication import RedirectToLoginException


class CustomAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except RedirectToLoginException as e:
            return e.args[0]  # This is the HttpResponseRedirect

        return response
