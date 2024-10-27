import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from home.models import Vps, VpsStatus

from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer, CachedCluster
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.invoice import InvoiceRepository
from services.virtualizor_manager import VirtualizorManager
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_plan(request):
    user = request.user
    if not user.is_staff:
        return JsonResponse('Permission denied', safe=False)

    cluster_name = request.GET.get('cluster_name')

    plans = CachedPlan().get()
    clusters = CachedCluster().get()
    unique_cluster_name = list(set([cluster.get('name') for cluster in clusters]))
    clusters = {cluster['id']: cluster for cluster in clusters}

    for plan in plans:
        cluster = clusters.get(plan['cluster_id'], {})
        if cluster:
            plan['cluster'] = cluster
            plan['cluster_name'] = cluster.get('name')

    if cluster_name:
        plans = [plan for plan in plans if plan.get('cluster_name') == cluster_name]

    return JsonResponse({
        'meta_data': {
            'list_cluster': unique_cluster_name
        },
        'data': plans,
        'total_pages': 1,
        'current_page': 1,
        'has_next': False,
        'has_previous': False,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def set_price(request):
    user = request.user
    if not user.is_staff:
        return JsonResponse('Permission denied', safe=False)

    data = request.data
    plan_id = int(data.get('plan_id'))
    price = data.get('price')

    if not plan_id or not price:
        return JsonResponse('Invalid data', safe=False)

    plans = CachedPlan().get()
    plan = [plan for plan in plans if plan.get('id') == plan_id]
    if not plan:
        return JsonResponse('Plan not found', safe=False)

    virtualizor_manager = VirtualizorManager()
    virtualizor_manager.set_price(plan_id, price)

    CachedPlan().delete()

    return JsonResponse('Price set successfully', safe=False)