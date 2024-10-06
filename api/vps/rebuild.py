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
def rebuild_vps(request):
    data = json.loads(request.body)
    user = request.user
    vps_id = data.get('vps_id')
    vps_linked_id = data.get('linked_id')

    image_version = data.get('image_version')
    password = data.get('password')

    osid = None
    oses = CachedOS().get()
    for os in oses:
        if os['name'] == image_version:
            osid = os['id']
            break
    if not osid:
        return JsonResponse({'error': 'Invalid image version'}, status=400)

    username = "Administrator" if os.get('distro') == 'windows' else 'root'
    if vps_id:
        vps = Vps.objects.filter(id=vps_id)
    else:
        vps = Vps.objects.filter(linked_id=vps_linked_id)
    if not user.is_staff:
        vps.filter(user_id=user.id)
    vps = vps.first()

    if not vps or not osid:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    publisher = make_kafka_publisher(KafkaConfig)

    vps.status = VpsStatus.REBUILDING
    vps.password = password
    vps.username = username
    vps.os_version = os['name']
    vps.save()
    VPSLogger().log(user, vps, 'rebuild', VpsStatus.REBUILDING)
    payload = {
        "osid": osid,
        "vps_id": vps.id,
        "password": password,
        "raw_data": data,
        "username": username,

    }
    publisher.publish('rebuild_vps', payload)

    return JsonResponse({}, safe=False)
