# myapp/context_processors.py

from config import APPConfig, CustomInfo
from home.models import User


def my_constants(request):
    all_user = User.objects.filter(is_active=True).all()
    list_user = [user.username for user in all_user]
    list_email = [user.email for user in all_user]
    return {
        'APP_ROLE': APPConfig.APP_ROLE,
        "VND_USD_EXCHANGE_RATE": APPConfig.VND_USD_EXCHANGE_RATE,
        "APP_NAME": APPConfig.APP_NAME,
        "APP_DOMAIN": CustomInfo.APP_DOMAIN,
        "INVOICE_TERM_CONDITION": CustomInfo.INVOICE_TERM_CONDITION,
        "COMPANY_ADDRESS": CustomInfo.COMPANY_ADDRESS,
        "COMPANY_PHONE": CustomInfo.COMPANY_PHONE,
        "ALL_EMAIL": list_email,
        "ALL_USERNAME": list_user
    }