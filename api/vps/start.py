import time
import json
from datetime import datetime, timedelta

from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from api.vps.__base__ import apply_vps_status
from core import settings
from home.models import Vps, VpsStatus

from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer, CachedVpsStatRepository
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.invoice import InvoiceRepository
from services.vps import VPSService
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@extend_schema(
    request=dict,
    responses={200: dict},
    description="Start a VPS instance with specified parameters",
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "vps_ids": [
                    "your_vps_id"
                ]
            },
            request_only=True,  # this example only applies to the request body
        ),
        OpenApiExample(
            'Example Response',
            value={
                "status": "success",
                "message": 'VPS is starting'
            },
            response_only=True,  # this example only applies to the response
        )
    ]
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def start_vps(request):
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

    apply_vps_status(list_vps)

    for vps in list_vps:
        if vps.status not in [VpsStatus.OFF, VpsStatus.ERROR, VpsStatus.STOPPING]:
            continue
        vps.status = VpsStatus.STARTING
        vps.save()
        VPSLogger().log(user, vps, 'start', VpsStatus.STARTING)
        payload = {
            "vps_id": vps.id
        }
        publisher.publish('start_vps', payload)

    return JsonResponse({
        "status": "success",
        "message": 'VPS is starting'
    }
        , safe=False)
