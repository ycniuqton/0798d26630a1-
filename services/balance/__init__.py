from home.models import User, Balance, Transaction


class BalanceRepository:
    def __init__(self):
        pass

    def get_balance(self, user_id):
        try:
            balance = Balance.objects.get(user_id=user_id)
            return balance.to_readable_dict()
        except:
            return None

    def modify(self, user_id, amount, _type='topup'):
        user = User.objects.get(id=user_id)
        if not user:
            return None

        transaction = Transaction.objects.create(
            user_id=user_id,
            amount=amount,
            type=_type,
            balance_id=user.balance.id
        )

        balance = Balance.objects.get(user_id=user_id)
        balance.amount += amount
        balance.save()

        return transaction

    def topup(self, user_id, amount):
        return self.modify(user_id, amount, 'topup')

    def reclaim(self, user_id, amount):
        return self.modify(user_id, -amount, 'reclaim')

    def charge(self, user_id, amount):
        return self.modify(user_id, -amount, 'charge')
