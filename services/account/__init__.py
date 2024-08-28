from home.models import User, Balance, Transaction


class AccountRepository:
    def __init__(self):
        pass

    def get_account(self, account_id):
        return self.db.get_account(account_id)

    def create_account(self, account_id):
        self._create_balance(account_id)

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
