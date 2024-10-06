from datetime import timedelta

from django.db.models import Sum, Count

from home.models import TopUpReport, InvoicePaidReport, RefundReport, Transaction, OrderReport, Invoice, \
    UnpaidOrderReport


class BaseCounter:
    base_model = None

    def __init__(self):
        pass

    def add(self, executed_at, amount):
        date = executed_at.replace(hour=0, minute=0, second=0, microsecond=0)

        record = self.base_model.objects.get_or_create(date=date)
        record.amount += amount
        record.save()

    def update(self, executed_at):
        date = executed_at.replace(hour=0, minute=0, second=0, microsecond=0)

        record, _ = self.base_model.objects.get_or_create(date=date)
        record.amount = self.load_current_amount(date) or 0
        record.save()

    def load_current_amount(self, date):
        return 0

    def total(self):
        return self.base_model.objects.aggregate(Sum('amount'))['amount__sum'] or 0

    def total_in_range(self, start_date, end_date):
        return self.base_model.objects.filter(date__gte=start_date, date__lte=end_date).aggregate(Sum('amount'))[
            'amount__sum'] or 0

    def get(self, date):
        date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        data = self.base_model.objects.filter(date=date).first()
        if not data:
            return 0
        return data.amount

    def records(self, start_date, end_date):
        return self.base_model.objects.filter(date__gte=start_date, date__lte=end_date).all() or []


class TopUpCounter(BaseCounter):
    base_model = TopUpReport

    def load_current_amount(self, date):
        from_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        from_time = from_time - timedelta(hours=7)
        to_time = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        to_time = to_time - timedelta(hours=7)
        total = \
            Transaction.objects.filter(type='topup', _created__lt=to_time, _created__gte=from_time).aggregate(
                Sum('amount'))[
                'amount__sum']

        return total


class InvoicePaidCounter(BaseCounter):
    base_model = InvoicePaidReport

    def load_current_amount(self, date):
        from_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        from_time = from_time - timedelta(hours=7)
        to_time = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        to_time = to_time - timedelta(hours=7)
        total = \
            Transaction.objects.filter(type='charge', _created__lt=to_time, _created__gte=from_time).aggregate(
                Sum('amount'))[
                'amount__sum']
        if not total:
            total = 0
        return 0 - total


class OrderCounter(BaseCounter):
    base_model = OrderReport

    def load_current_amount(self, date):
        from_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        from_time = from_time - timedelta(hours=7)
        to_time = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        to_time = to_time - timedelta(hours=7)
        total = \
            Invoice.objects.filter(status=Invoice.Status.PAID, _created__lt=to_time, _created__gte=from_time).aggregate(
                Count('id'))[
                'id__count']
        if not total:
            total = 0
        return total


class UnpaidOrderCounter(BaseCounter):
    base_model = UnpaidOrderReport

    def load_current_amount(self, date):
        from_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        from_time = from_time - timedelta(hours=7)
        to_time = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        to_time = to_time - timedelta(hours=7)
        total = \
            Invoice.objects.filter(status=Invoice.Status.OPEN, _created__lt=to_time, _created__gte=from_time).aggregate(
                Count('id'))[
                'id__count']
        if not total:
            total = 0
        return total


class RefundCounter(BaseCounter):
    base_model = RefundReport

    def load_current_amount(self, date):
        from_time = date.replace(hour=0, minute=0, second=0, microsecond=0)
        from_time = from_time - timedelta(hours=7)
        to_time = date.replace(hour=23, minute=59, second=59, microsecond=999999)
        to_time = to_time - timedelta(hours=7)
        total = \
            Transaction.objects.filter(type='refund', _created__lt=to_time, _created__gte=from_time).aggregate(
                Sum('amount'))[
                'amount__sum']

        return total
