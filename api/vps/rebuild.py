import time
import json
from datetime import datetime, timedelta

from drf_spectacular.utils import extend_schema, OpenApiExample
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


@extend_schema(
    request=dict,
    responses={200: dict},
    description="Rebuild a VPS instance with specified parameters",
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "vps_id": "25de1b45-e8a5-4c08-8d3a-7626f724112e",
                "image_version": "ubuntu-18.04-x86_64x",
                "password": "Abcd@123ab"
            },
            request_only=True,  # this example only applies to the request body
        ),
        OpenApiExample(
            'Example Response',
            value={"status": "success", "message": 'VPS is rebuilding'},
            response_only=True,  # this example only applies to the response
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rebuild_vps(request):
    data = json.loads(request.body)
    user = request.user
    vps_id = data.get('vps_id')
    vps_linked_id = data.get('linked_id')

    image_version = data.get('image_version')
    password = data.get('password')

    if vps_id:
        vps = Vps.objects.filter(id=vps_id)
    else:
        vps = Vps.objects.filter(linked_id=vps_linked_id)

    if not user.is_staff:
        vps.filter(user_id=user.id)
    vps = vps.first()

    if not vps:
        return JsonResponse({'error': 'Invalid VPS'}, status=400)

    osid = None
    oses = CachedOS().get()
    for os in oses:
        if os['name'] == image_version and os['cluster_id'] == vps.region.get('cluster_id'):
            osid = os['id']
            break
    if not osid:
        return JsonResponse({'error': 'Invalid image version'}, status=400)

    username = "Administrator" if os.get('distro') == 'windows' else 'root'

    if not vps or not osid:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    publisher = make_kafka_publisher(KafkaConfig)

    vps.status = VpsStatus.REBUILDING
    vps.password = password
    vps.username = username
    vps.os_version = os['name']
    vps.os = os['distro']
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

    return JsonResponse({"status": "success", "message": 'VPS is rebuilding'}, status=200)
