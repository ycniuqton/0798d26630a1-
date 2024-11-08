# myapp/context_processors.py

from config import APPConfig, CustomInfo


def my_constants(request):
    """
    A context processor that adds the MY_CONSTANT setting to the context.
    """
    return {
        'APP_ROLE': APPConfig.APP_ROLE,
        "VND_USD_EXCHANGE_RATE": APPConfig.VND_USD_EXCHANGE_RATE,
        "APP_NAME": APPConfig.APP_NAME,
        "APP_DOMAIN": CustomInfo.APP_DOMAIN,
        "INVOICE_TERM_CONDITION": CustomInfo.INVOICE_TERM_CONDITION,
        "COMPANY_ADDRESS": CustomInfo.COMPANY_ADDRESS,
        "COMPANY_PHONE": CustomInfo.COMPANY_PHONE,

    }