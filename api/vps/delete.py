import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from api.vps.__base__ import apply_vps_status
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
def delete_vps(request):
    data = json.loads(request.body)
    user = request.user
    vps_ids = data.get('vps_ids', [])
    vps_linked_ids = data.get('linked_ids', [])

    if vps_ids:
        list_vps = Vps.objects.filter(id__in=vps_ids)
    else:
        list_vps = Vps.objects.filter(linked_id__in=vps_linked_ids)
    if not user.is_staff:
        list_vps.filter(user_id=user.id)
    list_vps = list(list_vps)

    publisher = make_kafka_publisher(KafkaConfig)
    for vps in list_vps:
        vps.status = VpsStatus.DELETING
        vps.save()
        VPSLogger().log(user, vps, 'delete', VpsStatus.DELETING)
        payload = {
            "vps_id": vps.id
        }
        publisher.publish('delete_vps', payload)

    return JsonResponse('VPS is deleting', safe=False)



