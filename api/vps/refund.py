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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def refund_vps(request, vps_id):
    user = request.user

    vps = Vps.objects.filter(id=vps_id)
    if not user.is_staff:
        vps.filter(user_id=user.id)
    vps = vps.first()

    if not vps:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    if not vps.is_refundable:
        return JsonResponse({'error': 'VPS is not refundable'}, status=400)

    publisher = make_kafka_publisher(KafkaConfig)

    vps.status = VpsStatus.REFUND_REQUESTED
    vps.save()
    payload = {
        "vps_id": vps.id,

    }
    publisher.publish('refund_vps', payload)

    return JsonResponse({}, safe=False)
