from adapters.redis_service import CachedVpsStatRepository
from core import settings
from home.models import VpsStatus
from services.vps import VPSService


def apply_vps_status(list_vps):
    for vps in list_vps:
        stat = VPSService(settings.ADMIN_CONFIG.URL, settings.ADMIN_CONFIG.API_KEY).stat(vps.linked_id)
        if not stat:
            continue

        status = stat.get('status')
        if status == 1:
            vps.status = VpsStatus.ON
        elif status == 0:
            vps.status = VpsStatus.OFF
        elif status == 2:
            vps.status = VpsStatus.SUSPENDED
        CachedVpsStatRepository().set(vps.linked_id, stat)
        vps.save()
