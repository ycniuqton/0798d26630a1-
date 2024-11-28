import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from core import settings
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
def update_info(request, vps_id):
    data = json.loads(request.body)
    user = request.user
    linked_id = data.get('linked_id')
    updatable_fields = ['auto_renew']
    new_data = {}
    for field in updatable_fields:
        if field in data:
            new_data[field] = data[field]

    if linked_id:
        vps = Vps.objects.filter(linked_id=linked_id).first()
    else:
        vps = Vps.objects.get(id=vps_id)

    if not vps:
        return JsonResponse('Invalid Request', safe=False)
    if not user.is_staff and vps.user_id != user.id:
        return JsonResponse('Permission denied', safe=False)

    for field, value in new_data.items():
        setattr(vps, field, value)

    vps.save()

    if 'hostname' in new_data:
        publisher = make_kafka_publisher(KafkaConfig)
        publisher.publish('change_hostname_vps', {
            'vps_id': vps.id,
            'hostname': new_data['hostname']
        })

    return JsonResponse('', safe=False)
