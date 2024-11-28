from config import KafkaNotifierConfig
from .__handlers__ import *
from adapters.kafka_adapter import HandlerFactory
from adapters.kafka_adapter.consumer import KafkaListener


class VirtualizorEvent:
    PLAN_RELOADED = 'plan_reloaded'
    SERVER_RELOADED = 'server_reloaded'
    GROUP_RELOADED = 'group_reloaded'

    # VPS
    VPS_CREATED = 'vps_created'
    VPS_CREATED_FAILED = 'vps_created_failed'
    VPS_TURNED_ON = 'vps_turned_on'
    VPN_TURNED_ON_FAILED = 'vps_turned_on_failed'
    VPS_TURNED_OFF = 'vps_turned_off'
    VPS_TURNED_OFF_FAILED = 'vps_turned_off_failed'
    VPS_SUSPENDED = 'vps_suspended'
    VPS_SUSPENDED_FAILED = 'vps_suspended_failed'
    VPS_UNSUSPENDED = 'vps_unsuspended'
    VPS_UNSUSPENDED_FAILED = 'vps_unsuspended_failed'
    VPS_RESTARTED = 'vps_restarted'
    VPS_RESTARTED_FAILED = 'vps_restarted_failed'
    VPS_REBUILT = 'vps_rebuilt'
    VPS_REBUILT_FAILED = 'vps_rebuilt_failed'
    VPS_DELETED = 'vps_deleted'
    VPS_DELETED_FAILED = 'vps_deleted_failed'
    VPS_STOPPED = 'vps_stopped'
    VPS_STOPPED_FAILED = 'vps_stopped_failed'
    VPS_PASSWORD_CHANGED_FAILED = 'vps_password_changed_failed'
    VPS_PASSWORD_CHANGED = 'vps_password_changed'
    VPS_HOSTNAME_CHANGED = 'vps_hostname_changed'
    VPS_HOSTNAME_CHANGED_FAILED = 'vps_hostname_changed_failed'




handlers = {
    VirtualizorEvent.VPS_CREATED: VPSCreated(),
    VirtualizorEvent.VPS_CREATED_FAILED: VPSCreatedError(),
    VirtualizorEvent.VPS_TURNED_ON: VPSStarted(),
    VirtualizorEvent.VPN_TURNED_ON_FAILED: VPSStartedError(),
    VirtualizorEvent.VPS_TURNED_OFF: VPSStopped(),
    VirtualizorEvent.VPS_TURNED_OFF_FAILED: VPSStoppedError(),
    VirtualizorEvent.VPS_SUSPENDED: VPSSuspended(),
    VirtualizorEvent.VPS_SUSPENDED_FAILED: VPSSuspendedError(),
    VirtualizorEvent.VPS_UNSUSPENDED: VPSUnSuspended(),
    # VirtualizorEvent.VPS_UNSUSPENDED_FAILED: VPSUnSuspendedError(),
    VirtualizorEvent.VPS_RESTARTED: VPSRestarted(),
    VirtualizorEvent.VPS_RESTARTED_FAILED: VPSRestartedError(),
    VirtualizorEvent.VPS_REBUILT: VPSRebuilt(),
    VirtualizorEvent.VPS_REBUILT_FAILED: VPSRebuiltError(),
    VirtualizorEvent.VPS_DELETED: VPSDeleted(),
    # VirtualizorEvent.VPS_DELETED_FAILED: VPSDeletedError(),
    VirtualizorEvent.VPS_PASSWORD_CHANGED: VPSChangedPassword(),
    VirtualizorEvent.VPS_HOSTNAME_CHANGED: VPSChangedHostname(),
    "cache_cleaned": CacheCleaned(),
    "agen_sync": AgencySync(),
}


def run():
    handler_factory = HandlerFactory(handlers=handlers)
    listener = KafkaListener(
        KafkaNotifierConfig,
        handler_factory=handler_factory,
    )
    listener.listen()
