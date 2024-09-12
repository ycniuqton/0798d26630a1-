import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from home.models import Vps

from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer, CachedServerGroup
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.invoice import InvoiceRepository
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_vps(request):
    data = json.loads(request.body)
    user = request.user

    hostname = data.get('login', {}).get('hostname', f'hostname-{time.time()}')
    password = data.get('login', {}).get('password', f'default-{time.time()}')
    username = data.get('login', {}).get('username', f'default-{time.time()}')
    sg_id = data.get('location', {}).get('id', 0)
    identifier = data.get('identifier', '')

    plid = data.get('plan', {}).get('id', 0)
    image_version = data.get('image', {}).get('version', 'None')
    duration = data.get('duration', 1)

    osid = None
    plans = CachedPlan().get()
    server_groups = CachedServerGroup().get()
    oses = CachedOS().get()
    for os in oses:
        if os['name'] == image_version:
            osid = os['id']
            break
    try:
        plan = [plan for plan in plans if plan['id'] == int(plid)][0]
    except:
        plan = None

    try:
        server_group = [sg for sg in server_groups if sg['id'] == int(sg_id)][0]
    except:
        server_group = None

    if not osid or not plan or not server_group:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    total_fee = plan['price'] * duration
    end_time = datetime.utcnow() + timedelta(days=30*duration)
    if user.balance.amount < total_fee and not user.is_staff:
        return JsonResponse({'error': 'Insufficient balance'}, status=400)

    vps = Vps(
        cpu=plan['cpu'],
        ram=plan['ram'],
        disk=plan['disk'],
        network_speed=plan['network_speed'],
        bandwidth=plan['bandwidth'],
        hostname=hostname,
        password=password,
        username=username,
        virt='kvm',
        plan_id=plan['id'],
        user_id=user.id,
        os_version=image_version,
        location=server_group['name'],
        os=os['distro'],
        end_time=end_time,
        identifier=identifier
    )
    vps.save()
    vps.plan = plan

    invoice_repo = InvoiceRepository()
    invoice = invoice_repo.create(user.id, items=[vps])
    invoice_repo.charge(invoice)

    VPSLogger().log(user, vps, 'create', 'creating')

    try:
        payload = {
            "hostname": hostname,
            "password": password,
            # "serid": serid,
            "plid": plid,
            "osid": str(osid),
            "vps_id": vps.id,
            "raw_data": data,
            "server_group": server_group['id'],
            "identifier": identifier,
        }
        publisher = make_kafka_publisher(KafkaConfig)
        publisher.publish('create_vps', payload)
        response_data = {
            'status': 'success',
            'message': 'VPS created successfully',
            'vpsConfiguration': data
        }
        return JsonResponse(response_data)
    except:
        response_data = {
            'status': 'error',
            'message': 'Failed to create VPS',
            'vpsConfiguration': {}
        }
        return JsonResponse(response_data)

    return JsonResponse({'error': 'Invalid request'}, status=400)
