from home.models import User, Balance, Transaction, AppSetting


class AppSettingRepository:
    def __init__(self):
        setting = AppSetting.objects.first()
        if not setting:
            setting = AppSetting.objects.create()
        self._INVOICE_DUE_DAYS = setting.invoice_due_days
        self._SUFFICIENT_BALANCE_SUSPEND_DAYS = setting.sufficient_balance_suspend_days

    @property
    def INVOICE_DUE_DAYS(self):
        return self._INVOICE_DUE_DAYS

    @property
    def SUFFICIENT_BALANCE_SUSPEND_DAYS(self):
        return self._SUFFICIENT_BALANCE_SUSPEND_DAYS

    @INVOICE_DUE_DAYS.setter
    def INVOICE_DUE_DAYS(self, value):
        self._INVOICE_DUE_DAYS = value
        AppSetting.objects.update(invoice_due_days=value)

    @SUFFICIENT_BALANCE_SUSPEND_DAYS.setter
    def SUFFICIENT_BALANCE_SUSPEND_DAYS(self, value):
        self._SUFFICIENT_BALANCE_SUSPEND_DAYS = value
        AppSetting.objects.update(sufficient_balance_suspend_days=value)

    def to_dict(self):
        return {
            'invoice_due_days': self.INVOICE_DUE_DAYS,
            'sufficient_balance_suspend_days': self.SUFFICIENT_BALANCE_SUSPEND_DAYS
        }
