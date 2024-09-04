import uuid
from django.utils import timezone

from home.models import User, Balance, Transaction, UserToken


class AccountRepository:
    def __init__(self):
        pass

    def get_account(self, account_id):
        return self.db.get_account(account_id)

    def create_account(self, account_id):
        self._create_balance(account_id)
        utr = UserTokenRepository()
        utr.create_token(account_id, description="Default token", ttl=-1, is_default=True)

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
