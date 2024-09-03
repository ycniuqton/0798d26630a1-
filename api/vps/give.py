import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from home.models import Vps, VpsStatus, User

from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.invoice import InvoiceRepository
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def give_vps(request):
    data = json.loads(request.body)
    user = request.user
    vps_ids = data.get('vps_ids', [])
    receiver = data.get('user_email', None)

    receiver = User.objects.filter(email=receiver).first()

    if not receiver or receiver.email == user.email:
        return JsonResponse('User not found', safe=False)

    list_vps = Vps.objects.filter(id__in=vps_ids)
    if not user.is_staff:
        list_vps.filter(user_id=user.id)
    list_vps = list(list_vps)

    publisher = make_kafka_publisher(KafkaConfig)
    for vps in list_vps:
        # if vps.status != VpsStatus.OFF:
        #     continue
        VPSLogger().log(user, vps, 'give', 'give', f'Give VPS to {receiver.email}')
        payload = {
            "vps_id": vps.id,
            'receiver_id': receiver.id,
        }
        publisher.publish('give_vps', payload)

    return JsonResponse('VPS is giving', safe=False)