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
def change_vps_plan(request, vps_id):
    data = json.loads(request.body)
    user = request.user
    plan_id = data.get('plan_id')

    plan = None
    plans = CachedPlan().get()
    try:
        plan = [plan for plan in plans if plan['id'] == int(plan_id)][0]
    except:
        plan = None

    vps = Vps.objects.filter(id=vps_id)
    if not user.is_staff:
        vps.filter(user_id=user.id)
    vps = vps.first()

    if not vps or not plan:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    publisher = make_kafka_publisher(KafkaConfig)

    vps.status = VpsStatus.REBUILDING
    vps.save()
    VPSLogger().log(user, vps, 'rebuild', VpsStatus.REBUILDING)
    payload = {
        "vps_id": vps.id,

    }
    publisher.publish('rebuild_vps', payload)

    return JsonResponse({}, safe=False)
