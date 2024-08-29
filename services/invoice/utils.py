from datetime import datetime, timedelta


def get_billing_cycle(time_point=datetime.utcnow):
    return time_point.strftime('%Y-%m')
