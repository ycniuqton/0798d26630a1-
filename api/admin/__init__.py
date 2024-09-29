import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from adapters.kafka_adapter import make_kafka_publisher
from adapters.redis_service.resources.full_data_server_group import CachedServerGroupConfig
from config import KafkaConfig, APPConfig
from home.models import Vps, User
from django.http import JsonResponse, HttpResponse

from services.app_setting import AppSettingRepository
from services.balance import BalanceRepository


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_configs(request):
    user = request.user
    if not user.is_staff or APPConfig.APP_ROLE != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    group_configs = CachedServerGroupConfig().get()

    return JsonResponse(group_configs)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def lock_group(request):
    user = request.user
    if not user.is_staff or APPConfig.APP_ROLE != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)

    data = json.loads(request.body)
    group_id = data.get('group_id')
    server_id = data.get('server_id')
    is_locked = data.get('is_locked')

    group_configs = CachedServerGroupConfig().get()
    for k, v in group_configs.items():
        if k == group_id:
            v['is_locked'] = is_locked
            if server_id and server_id in v['servers']:
                v['servers'][server_id]['is_locked'] = is_locked
            if not is_locked:
                for server_id, server in v['servers'].items():
                    v['servers'][server_id]['is_locked'] = False

    CachedServerGroupConfig().set(group_configs)
    return JsonResponse({'message': 'Lock success'})


class SuspendConfig(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        app_setting = AppSettingRepository().to_dict()

        return JsonResponse(app_setting)

    def post(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = request.data
        invoice_due_days = data.get('invoice_due_days')
        sufficient_balance_suspend_days = data.get('sufficient_balance_suspend_days')
        app_setting = AppSettingRepository()
        app_setting.INVOICE_DUE_DAYS = invoice_due_days
        app_setting.SUFFICIENT_BALANCE_SUSPEND_DAYS = sufficient_balance_suspend_days

        return JsonResponse({'message': 'Update success'})
