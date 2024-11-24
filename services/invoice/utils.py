from datetime import datetime, timedelta

from django.utils import timezone


def get_billing_cycle(from_time=datetime.utcnow, type='monthly', num=1, to_time=None):
    if not to_time:
        if type == 'monthly':
            if from_time.month + num > 12:
                to_time = from_time.replace(year=from_time.year + (from_time.month + num - 1) // 12,
                                            month=(from_time.month + num) % 12)
            else:
                to_time = from_time.replace(month=from_time.month + num)
        elif type == 'yearly':
            to_time = from_time.replace(year=from_time.year + num)
    return f"{from_time.strftime('%Y-%m-%d')}:{to_time.strftime('%Y-%m-%d')}", from_time, to_time


def get_now():
    return datetime.now(timezone.utc)
