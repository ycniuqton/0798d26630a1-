import uuid
from django.utils import timezone
from core import settings
from django.contrib.auth import get_user_model
from home.models import User, Balance, Transaction, UserToken
from services.mail_service import VPSMailService


class AccountRepository:
    def __init__(self):
        pass

    def get_account(self, account_id):
        return self.db.get_account(account_id)

    def create_account_business_logic(self, user_id):
        self._create_balance(user_id)
        utr = UserTokenRepository()
        utr.create_token(user_id, description="Default token", ttl=-1, is_default=True)

    def setup_new_user(self, user, send_email=True):
        """Helper method to setup a new user account and send welcome email"""
        self.create_account_business_logic(user.id)
        if send_email and settings.APPConfig.APP_ROLE != 'admin':
            VPSMailService().send_register_email(user)
        return user

    def create_user_from_oauth(self, email, first_name='', last_name='', **extra_fields):
        """Create a new user from OAuth data with unique username"""
        User = get_user_model()
        username = email.split('@')[0]
        base_username = username
        counter = 1

        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )

        return self.setup_new_user(user)

    def _create_balance(self, account_id):
        user = User.objects.get(id=account_id)
        balance = Balance()
        balance.user = user
        balance.amount = 0
        balance.save()

        transaction = Transaction()
        transaction.user = user
        transaction.amount = 0
        transaction.type = "credit"
        transaction.status = "success"
        transaction.description = "Initial balance"
        transaction.balance = balance
        transaction.save()

    def update_account(self, account):
        return self.db.update_account(account)

    def delete_account(self, account_id):
        return self.db.delete_account(account_id)


class UserTokenRepository:
    def __init__(self):
        self.db = UserToken
        pass

    def create_token(self, user_id, description="", ttl=0, is_default=False):
        user_token = UserToken()
        user_token.user_id = user_id
        user_token.token = str(uuid.uuid4())
        user_token.is_default = is_default
        user_token.description = description
        user_token.ttl = ttl
        expired_at = timezone.now() + timezone.timedelta(seconds=ttl)
        user_token.expired_at = expired_at
        user_token.save()
        return user_token

    def get_token(self, user_id):
        return self.db.get_token(user_id)

    def delete_token(self, token_id):
        user_token = UserToken.objects.get(id=token_id)
        if user_token.is_default:
            return False
        else:
            user_token.delete()
            return True
