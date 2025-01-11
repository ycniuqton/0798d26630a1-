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
from config import KafkaConfig, KafkaNotifierConfig
from services.invoice import InvoiceRepository
from services.vps import VPSService
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_vps_end_time(request):
    data = json.loads(request.body)
    user = request.user
    vps_id = data.get('vps_id')
    vps_linked_id = data.get('linked_id')
    end_time = data.get('end_time')

    if vps_id:
        vps = Vps.objects.filter(id=vps_id).first()
    else:
        vps = Vps.objects.filter(linked_id=vps_linked_id).first()

    if not user.is_superuser and settings.APPConfig.APP_ROLE != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)

    if settings.APPConfig.APP_ROLE != 'admin':
        from services.vps import CtvVPSService
        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY
        vps_service = CtvVPSService(base_url, api_key)
        vps_service.update_vps_end_time(vps.linked_id, end_time)
    else:
        publisher = make_kafka_publisher(KafkaNotifierConfig)
        publisher.publish('set_vps_end_time', {
            'identifier': vps.linked_id,
            'end_time': end_time
        })

    return JsonResponse({'status': 'success', 'message': 'VPS end time is updated'})