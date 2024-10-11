from datetime import timedelta, datetime

from adapters.redis_service import CachedPlan
from home.models import User, Balance, Transaction, Invoice, InvoiceLine
from services.app_setting import AppSettingRepository
from services.balance import BalanceRepository
from services.discount import DiscountRepository
from services.invoice.utils import get_billing_cycle, get_now


class InvoiceRepository:
    def __init__(self):
        pass

    def gen_code(self, user_id):
        now = get_now()
        return f"{user_id[-4:]}-{now.month}-{now.year}-{now.microsecond}"

    def create(self, user_id, items=[], cycle=None, from_time=None, to_time=None, duration=1):
        if not duration:
            duration = 1
        user = User.objects.get(id=user_id)

        plans = CachedPlan().get()
        discount_repo = DiscountRepository.get(duration=duration)

        # apply price
        for item in items:
            plan = next((p for p in plans if p.get('id') == item.plan_id), None)
            if not plan:
                item.price = 0
                item.plan_name = ""
            else:
                item.price = plan.get('price', 0) * duration
                item.price, _ = discount_repo.apply(item.price)
                item.plan_name = plan.get('name', "")

        total_fee = sum([i.price for i in items])
        now = get_now()
        code = self.gen_code(user.id)

        if not cycle:
            cycle, from_time, to_time = get_billing_cycle(now)

        app_setting = AppSettingRepository()

        invoice = Invoice.objects.create(
            user=user,
            code=code,
            amount=total_fee,
            status=Invoice.Status.OPEN,
            description="Initial invoice",
            transaction=None,
            due_date=now + timedelta(days=app_setting.INVOICE_DUE_DAYS),
            cycle=cycle,
            start_time=from_time,
            end_time=to_time,
        )

        for item in items:
            invoice_line = InvoiceLine.objects.create(
                invoice=invoice,
                vps=item,
                amount=item.price,
                description=f"VPS {item.plan_name}",
                start_time=from_time,
                end_time=to_time,
                cycle=cycle,
            )

        return invoice

    def refund(self, user, invoice_lines):
        amount = 0 - sum([i.amount for i in invoice_lines])
        code = self.gen_code(user.id)
        now = get_now()
        cycle, from_time, to_time = get_billing_cycle(now)

        invoice = Invoice.objects.create(
            user=user,
            code=code,
            amount=amount,
            status=Invoice.Status.OPEN,
            description="Initial invoice",
            transaction=None,
            due_date=now + timedelta(days=1),
            cycle=cycle,
            start_time=from_time,
            end_time=to_time,
        )

        for item in invoice_lines:
            invoice_line = InvoiceLine.objects.create(
                invoice=invoice,
                vps=item.vps,
                amount=0-item.amount,
                description=f"Refund {item.vps}",
                start_time=from_time,
                end_time=to_time,
                cycle=cycle,
            )

        return invoice

    def charge(self, invoice):
        if invoice.status != Invoice.Status.OPEN:
            return True
        user = invoice.user
        if user.balance.amount < invoice.amount:
            return False

        balance_repo = BalanceRepository()
        transaction = balance_repo.charge(user.id, invoice.amount)

        invoice.status = Invoice.Status.PAID
        invoice.transaction = transaction
        invoice.save()

        return True
