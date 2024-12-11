import json
from functools import reduce

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from adapters.kafka_adapter import make_kafka_publisher
from adapters.redis_service import clear_cache, CachedCluster, CachedServerGroup, CachedPlanInRegion
from adapters.redis_service.resources.full_data_server_group import CachedServerGroupConfig
from config import KafkaConfig, APPConfig, KafkaNotifierConfig
from home.models import Vps, User, RefundRequest
from django.http import JsonResponse, HttpResponse

from services.app_setting import AppSettingRepository
from services.balance import BalanceRepository
from services.cluster import ClusterManager
from services.vps.refund import RefundService


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_group_configs(request):
    user = request.user
    if not user.is_staff or APPConfig.APP_ROLE != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)
    group_configs = CachedServerGroup().get()

    return JsonResponse(group_configs, safe=False)


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


class VpsConfig(APIView):
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
        vps_auto_archive = data.get('vps_auto_archive')
        app_setting = AppSettingRepository()
        app_setting.VPS_AUTO_ARCHIVE = vps_auto_archive

        return JsonResponse({'message': 'Update success'})


class RefundRequestAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        filterable_fields = ['status']
        search_fields = []
        sortable_fields = []
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        sort_by = request.GET.get('sort_by', '-_created')
        sort_by = sort_by if sort_by in sortable_fields else '-_created'
        filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
        search_value = request.GET.get('search')
        search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                        ]
        if search_query:
            search_query = reduce(lambda x, y: x | y, search_query)
        else:
            search_query = Q()

        objects = RefundRequest.objects.filter(**filters).filter(search_query)

        total = objects.count()

        objects = objects.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        data = [data.to_readable_dict() for data in objects]

        return JsonResponse({
            'data': data,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def approve_refund_request(request, request_id):
    user = request.user
    if not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    refund_request = RefundRequest.objects.filter(id=request_id,
                                                  status=RefundRequest.RefundRequestStatus.PENDING).first()

    if not refund_request:
        return JsonResponse({'error': 'Refund request not found'}, status=404)

    rs = RefundService()
    rs.approve(refund_request)

    return JsonResponse({'message': 'Refund request approved'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reject_refund_request(request, request_id):
    user = request.user
    if not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    refund_request = RefundRequest.objects.filter(id=request_id,
                                                  status=RefundRequest.RefundRequestStatus.PENDING).first()

    if not refund_request:
        return JsonResponse({'error': 'Refund request not found'}, status=404)

    rs = RefundService()
    rs.reject(refund_request)

    return JsonResponse({'message': 'Refund request rejected'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def admin_clear_cache(request):
    user = request.user
    if not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = None

    if not data:
        publisher = make_kafka_publisher(KafkaNotifierConfig)
        publisher.publish('cache_cleaned', {})

        clear_cache(True, True, True, True, True, True)
    else:
        plan = data.get('plan', False)
        os = data.get('os', False)
        server = data.get('server', False)
        server_group = data.get('server_group', False)
        full_server_group = data.get('full_server_group', False)
        cluster = data.get('cluster', False)

        clear_cache(plan, os, server, server_group, full_server_group, cluster)

    return JsonResponse({'message': 'Cache cleared'})


class ClusterResource(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached_cluster = CachedCluster().get()

        return JsonResponse({
            'data': cached_cluster,
            'total_pages': 1,
            'current_page': 1,
            'has_next': False,
            'has_previous': False,
        })

    def post(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = request.data
        updatable_fields = ['name', 'ip', 'api_key', 'api_pass', 'user_api_key', 'user_api_pass']
        data = {field: data.get(field) for field in updatable_fields}

        cluster_manager = ClusterManager()
        res = cluster_manager.create_cluster(**data)

        return JsonResponse(res, safe=False)


class GroupResource(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached_cluster = CachedCluster().get()
        mapping_cluster = {cluster['id']: cluster for cluster in cached_cluster}
        cached_group = CachedServerGroup().get()

        for group in cached_group:
            group['cluster'] = mapping_cluster.get(group['cluster_id'])
            group['list_plan'] = CachedPlanInRegion().get(group['id']) if CachedPlanInRegion().get(group['id']) else []

        lock_config = AppSettingRepository().REGION_LOCKED_CONFIG
        for group in cached_group:
            locked = lock_config.get(str(group['id']))
            if locked:
                group['is_locked'] = True
            else:
                group['is_locked'] = False

            for server in group['server']:
                if str(server.get('id')) == locked:
                    server['is_locked'] = True
                else:
                    server['is_locked'] = False

        return JsonResponse({
            'data': cached_group,
            'total_pages': 1,
            'current_page': 1,
            'has_next': False,
            'has_previous': False,
        })

    def post(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = request.data
        updatable_fields = ['name', 'country']
        group_id = data.get('id')
        locked = data.get('lock')
        list_plan = data.get('list_plan')

        data = {field: data.get(field) for field in updatable_fields}

        if not group_id:
            return JsonResponse({'error': 'Region id is required'}, status=400)

        res = CachedServerGroup().update(group_id, data)
        if locked:
            AppSettingRepository().lock_region(region_id=group_id, server_id=locked)
        else:
            AppSettingRepository().unlock_region(region_id=group_id)

        if list_plan is not None and isinstance(list_plan, list):
            list_plan = [int(i) for i in list_plan]
            CachedPlanInRegion().set(list_plan, group_id)

        # send clear cache message
        publisher = make_kafka_publisher(KafkaNotifierConfig)
        publisher.publish('cache_cleaned', {})

        return JsonResponse(res, safe=False)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_cluster(request):
    user = request.user
    if not user.is_staff or APPConfig.APP_ROLE != 'admin':
        return JsonResponse({'error': 'Permission denied'}, status=403)

    ip = request.data.get('ip')
    api_key = request.data.get('api_key')
    api_pass = request.data.get('api_pass')
    user_api_key = request.data.get('user_api_key')
    user_api_pass = request.data.get('user_api_pass')

    cluster_manager = ClusterManager()
    if cluster_manager.test_cluster(ip, api_key, api_pass, user_api_key, user_api_pass):
        return JsonResponse({'message': 'Test success', 'data': {'is_ok': True}})
    else:
        return JsonResponse({'message': 'Test failed', 'data': {'is_ok': False}}, status=400)
