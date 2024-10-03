import json
from functools import reduce

from django.db.models import Q
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from adapters.kafka_adapter import make_kafka_publisher
from adapters.redis_service import CachedVpsBackup
from config import KafkaConfig
from home.models import Vps, VpsStatus
from django.http import JsonResponse, HttpResponse

from services.vps_log import VPSLogger


class VpsSnapshotAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, vps_id):
        user = request.user
        vps = Vps.objects.filter(id=vps_id)
        if not user.is_staff:
            vps = vps.filter(user=user)
        vps = vps.first()
        if not vps:
            return JsonResponse({'error': 'VPS not found'}, status=404)

        vps_backup = CachedVpsBackup()
        vps_backup_data = vps_backup.get(str(vps.linked_id))
        vps_backup_data = vps_backup_data or []

        # update backup count
        if vps.backup_count != len(vps_backup_data):
            vps.backup_count = len(vps_backup_data)
            vps.save()

        return JsonResponse({
            'data': vps_backup_data,
            'total_pages': 1,
            'current_page': 1,
            'has_next': False,
            'has_previous': False,
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restore_vsp(request, vps_id):
    user = request.user
    data = json.loads(request.body)
    vps = Vps.objects.filter(id=vps_id)
    if not user.is_staff:
        vps = vps.filter(user=user)
    vps = vps.first()

    if not vps:
        return JsonResponse({'error': 'VPS not found'}, status=404)

    abs_path = data.get('abs_path')
    if not abs_path:
        return JsonResponse({'error': 'abs_path is required'}, status=400)

    VPSLogger().log(user, vps, action='restore', status=VpsStatus.RESTORING)

    publisher = make_kafka_publisher(KafkaConfig)
    publisher.publish('restore_vps', {
        'vps_id': vps.id,
        'abs_path': abs_path,
    })

    return JsonResponse({'message': 'Restoring VPS'})

