from datetime import timedelta, datetime

from home.models import User, Balance, Transaction, Invoice, InvoiceLine
from services.balance import BalanceRepository
from services.invoice.utils import get_billing_cycle


class InvoiceRepository:
    def __init__(self):
        pass

    def create(self, user_id, items=[]):
        user = User.objects.get(id=user_id)

        items = [i for i in items if i.plan]
        total_fee = sum([i.plan.get('price', 0) for i in items])
        now = datetime.utcnow()
        code = f"{user.id[-4:]}-{now.month}-{now.year}-{now.microsecond}"
        cycle = get_billing_cycle(now)
        invoice = Invoice.objects.create(
            user=user,
            code=code,
            amount=total_fee,
            status="open",
            description="Initial invoice",
            transaction=None,
            due_date=datetime.utcnow() + timedelta(days=5),
            cycle=cycle,
        )

        for item in items:
            invoice_line = InvoiceLine.objects.create(
                invoice=invoice,
                vps=item,
                amount=item.plan.get('price', 0),
                description=f"VPS {item.plan.get('name', 'Unknown')}",
                start_time=datetime.utcnow(),
                end_time=item.end_time,
            )

        return invoice

    def charge(self, invoice):
        user = invoice.user
        if user.balance.amount < invoice.amount:
            return False

        balance_repo = BalanceRepository()
        transaction = balance_repo.charge(user.id, invoice.amount)

        invoice.status = "paid"
        invoice.transaction = transaction
        invoice.save()

        return True
