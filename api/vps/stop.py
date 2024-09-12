import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from home.models import Vps, VpsStatus

from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.invoice import InvoiceRepository
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def stop_vps(request):
    data = json.loads(request.body)
    user = request.user
    vps_ids = data.get('vps_ids', [])

    list_vps = Vps.objects.filter(id__in=vps_ids)
    if not user.is_staff:
        list_vps.filter(user_id=user.id)
    list_vps = list(list_vps)

    publisher = make_kafka_publisher(KafkaConfig)
    for vps in list_vps:
        if vps.status not in [VpsStatus.ON, VpsStatus.STARTING, VpsStatus.ERROR]:
            continue
        vps.status = VpsStatus.STOPPING
        vps.save()
        VPSLogger().log(user, vps, 'stop', VpsStatus.STOPPING)
        payload = {
            "vps_id": vps.id
        }
        publisher.publish('stop_vps', payload)

    return JsonResponse('VPS is stopping', safe=False)