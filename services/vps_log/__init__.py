from home.models import VPSLog


class VPSLoggerAction:
    CREATE = 'create'
    DELETE = 'delete'
    SUSPEND = 'suspend'
    UNSUSPEND = 'unsuspend'
    REBOOT = 'reboot'
    START = 'start'
    STOP = 'stop'
    RESET = 'reset'
    REBUILD = 'rebuild'
    RESIZE = 'resize'
    REINSTALL = 'reinstall'
    CHANGE_OS = 'change_os'
    CHANGE_PLAN = 'change_plan'
    CHANGE_LOCATION = 'change_location'
    CHANGE_PASSWORD = 'change_password'
    CHANGE_HOSTNAME = 'change_hostname'
    CHANGE_USERNAME = 'change_username'
    CHANGE_IP = 'change_ip'

    @classmethod
    def values(cls):
        return [value for key, value in vars(cls).items() if
                not key.startswith('__') and not callable(value) and isinstance(value, str)]


class VPSLogger:
    model = VPSLog

    def __init__(self):
        self.actions = VPSLoggerAction.values()
        self.action_mapping = {
            i: getattr(self, i, self._log) for i in self.actions
        }

    @staticmethod
    def _log(user, vps, action, status, description=''):
        model = VPSLogger.model
        model.objects.create(vps_id=vps.id, action=action, status=status, user_id=user.id, description=description)

    def log(self, user, vps, action, status, description=''):
        handler = self.action_mapping.get(action, self._log)
        handler(user, vps, action, status, description)

    @staticmethod
    def _create(user, vps, action, status, description=''):
        VPSLog.objects.create(vps_id=vps.id, action=action, status=status, user_id=user.id, description=description)
