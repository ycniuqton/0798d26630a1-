from datetime import timedelta

from services.invoice import get_now
from services.report import TopUpCounter, InvoicePaidCounter, OrderCounter, RefundCounter


def run(days=100):
    for i in range(days):
        TopUpCounter().update(get_now() - timedelta(days=i))
        InvoicePaidCounter().update(get_now() - timedelta(days=i))
        OrderCounter().update(get_now() - timedelta(days=i))
        RefundCounter().update(get_now() - timedelta(days=i))