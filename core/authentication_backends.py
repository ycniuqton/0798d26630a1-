from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using either their username or email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()

        # Try to fetch the user by email first
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            # If no user with the given email, try username
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None

        # Check the password
        if user.check_password(password):
            return user
        return None
