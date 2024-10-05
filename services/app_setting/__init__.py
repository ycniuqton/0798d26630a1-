from home.models import User, Balance, Transaction, AppSetting


class AppSettingRepository:
    def __init__(self):
        setting = AppSetting.objects.first()
        if not setting:
            setting = AppSetting.objects.create()
        self._INVOICE_DUE_DAYS = setting.invoice_due_days
        self._SUFFICIENT_BALANCE_SUSPEND_DAYS = setting.sufficient_balance_suspend_days
        self._VPS_AUTO_ARCHIVE = setting.vps_auto_archive
        self._VPS_REFUND_HOURS = setting.vps_refund_hours

    @property
    def INVOICE_DUE_DAYS(self):
        return self._INVOICE_DUE_DAYS

    @property
    def VPS_REFUND_HOURS(self):
        return self._VPS_REFUND_HOURS

    @property
    def SUFFICIENT_BALANCE_SUSPEND_DAYS(self):
        return self._SUFFICIENT_BALANCE_SUSPEND_DAYS

    @property
    def VPS_AUTO_ARCHIVE(self):
        return self._VPS_AUTO_ARCHIVE

    @INVOICE_DUE_DAYS.setter
    def INVOICE_DUE_DAYS(self, value):
        self._INVOICE_DUE_DAYS = value
        AppSetting.objects.update(invoice_due_days=value)

    @VPS_REFUND_HOURS.setter
    def VPS_REFUND_HOURS(self, value):
        self._VPS_REFUND_HOURS = value
        AppSetting.objects.update(vps_refund_hours=value)

    @VPS_AUTO_ARCHIVE.setter
    def VPS_AUTO_ARCHIVE(self, value):
        self._VPS_AUTO_ARCHIVE = value
        AppSetting.objects.update(vps_auto_archive=value)

    @SUFFICIENT_BALANCE_SUSPEND_DAYS.setter
    def SUFFICIENT_BALANCE_SUSPEND_DAYS(self, value):
        self._SUFFICIENT_BALANCE_SUSPEND_DAYS = value
        AppSetting.objects.update(sufficient_balance_suspend_days=value)

    def to_dict(self):
        return {
            'invoice_due_days': self.INVOICE_DUE_DAYS,
            'sufficient_balance_suspend_days': self.SUFFICIENT_BALANCE_SUSPEND_DAYS,
            'vps_auto_archive': self.VPS_AUTO_ARCHIVE,
            'vps_refund_hours': self.VPS_REFUND_HOURS
        }
