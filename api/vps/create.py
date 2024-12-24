import time
import json
import uuid
from datetime import datetime, timedelta

from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from api.vps.__constants import LIFETIME
from home.models import Vps, VpsStatus, SystemCounter

from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer, CachedServerGroup
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig, APPConfig
from services.discount import DiscountRepository
from services.invoice import InvoiceRepository, get_billing_cycle
from services.invoice.utils import get_now
from services.purchase_estimator import PurchaseEstimator
from services.vps_log import VPSLogger
from services.balance import BalanceRepository


@extend_schema(
    request=dict,
    responses={200: dict},
    description="""Create a new VPS instance with the specified configuration.
    <br>
    
    The request body should contain the following fields:
    
    - `location`: The location where the VPS will be hosted.
    - `image`: The OS image to use for the VPS.
    - `plan`: The plan to use for the VPS.
    
    These fields get from `/api/vps/configurations` endpoint.
    All the configurations should be in the same cluster (cluster_id).
    
    """,
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "location": {
                    "id": "43"
                },
                "image": {
                    "version": "windows-10-rutgon1"
                },
                "plan": {
                    "id": "302"
                },
                "login": {
                    "username": "Administrator",
                    "password": "YourPassword@123",
                    "hostname": "your_hostname"
                },
                "duration": 1,
                "auto_renew": True,
                "identifier": "random_uuid"  # must be unique
            },
            request_only=True,  # this example only applies to the request body
        ),
        OpenApiExample(
            'Example Response',
            value={"status": "success",
                   "message": "VPS created successfully"},
            response_only=True,  # this example only applies to the response
        )
    ]
)
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
    if not identifier:
        identifier = uuid.uuid4().hex

    plid = data.get('plan', {}).get('id', 0)
    image_version = data.get('image', {}).get('version', 'None')
    duration = data.get('duration', 1)
    auto_renew = data.get('auto_renew', True)

    osid = None
    plans = CachedPlan().get()
    server_groups = CachedServerGroup().get()
    oses = CachedOS().get()

    try:
        plan = [plan for plan in plans if plan['id'] == int(plid)][0]
    except:
        plan = None

    if not plan:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    for os in oses:
        if os['name'] == image_version and os['cluster_id'] == plan['cluster_id']:
            osid = os['id']
            break

    try:
        server_group = [sg for sg in server_groups if sg['id'] == int(sg_id)][0]
    except:
        server_group = None

    if not osid or not plan or not server_group:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    now = get_now()
    if duration == LIFETIME:
        cycle, from_time, to_time = get_billing_cycle(from_time=now,
                                                      to_time=get_now().replace(year=now.year + 100))
    else:
        cycle, from_time, to_time = get_billing_cycle(from_time=get_now(), type='monthly', num=duration)

    purchase_estimator = PurchaseEstimator(request.user)
    is_valid, message, discounted_fee, discount_amount, total_fee = purchase_estimator.estimate(plan, os, duration)

    if not is_valid:
        return JsonResponse({'error': message}, status=400)


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
        identifier=identifier,
        auto_renew=auto_renew,
        region=server_group
    )
    vps.plan = plan
    if user.is_staff:
        vps.end_time = to_time

    vps.save()

    VPSLogger().log(user, vps, 'create', 'creating')

    publisher = make_kafka_publisher(KafkaConfig)

    if not user.is_staff:
        publisher.publish('gen_invoice', {
            'user_id': user.id,
            'items': [vps.id],
            'cycle': cycle,
            'from_time': from_time,
            'to_time': to_time,
            'duration': duration,
            'is_first_time': True
        })

    creating_payload = {
        "hostname": hostname,
        "password": password,
        # "serid": serid,
        "plid": plid,
        "osid": str(osid),
        "vps_id": vps.id,
        "raw_data": data,
        "server_group": server_group['id'],
        "identifier": identifier,
        "cluster_id": server_group['cluster_id']
    }

    publisher.publish('create_vps', creating_payload)
    response_data = {
        'status': 'success',
        'message': 'VPS created successfully'
    }
    return JsonResponse(response_data)


@extend_schema(
    responses={200: dict},
    description="""Get the available VPS configurations.""",
    examples=[
        OpenApiExample(
            'Example Response',
            value={
                "plans": [
                    {
                        "id": "302",
                        "name": "VPS 1",
                        "cpu": 1,
                        "ram": 1024,
                        "disk": 20,
                        "network_speed": 1000,
                        "bandwidth": 1000,
                        "price": 10,
                        "cluster_id": 1
                    }
                ],
                "locations": [
                    {
                        "id": "43",
                        "name": "Vietnam",
                        "cluster_id": 1
                    }
                ],
                "images": [
                    {
                        "id": "1",
                        "type": "kvm",
                        "distro": "windows",
                        "filename": "windows-10-rutgon1",
                        "fstype": "ext3",
                        "name": "windows-10-rutgon1",
                        "version": "windows-10-rutgon1",
                        "cluster_id": 1
                    }
                ]
            },
            response_only=True,  # this example only applies to the response
        )
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vps_configurations(request):
    cluster_filter = request.GET.get('cluster_id', None)

    plans = CachedPlan().get()
    server_groups = CachedServerGroup().get()
    oses = CachedOS().get()

    if cluster_filter:
        plans = [plan for plan in plans if plan['cluster_id'] == int(cluster_filter)]
        server_groups = [sg for sg in server_groups if sg['cluster_id'] == int(cluster_filter)]
        oses = [os for os in oses if os['cluster_id'] == int(cluster_filter)]

    # exclude some fields from the response
    for region in server_groups:
        if isinstance(region, dict):
            region.pop('server', None)
    for image in oses:
        image['version'] = image.get('name')

    response_data = {
        'plans': plans,
        'locations': server_groups,
        'images': oses
    }
    return JsonResponse(response_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def re_create(request, vps_id):
    user = request.user
    vps = Vps.objects.get(id=vps_id)
    if vps.user_id != user.id and not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    if vps.status != VpsStatus.ERROR:
        return JsonResponse({'error': 'Cannot re-create this VPS'}, status=403)
    else:
        vps.status = VpsStatus.CREATING
        vps.save()

    publisher = make_kafka_publisher(KafkaConfig)
    if vps.creation_data:
        publisher.publish('create_vps', vps.creation_data)

    response_data = {
        'status': 'success',
        'message': 'VPS re-created successfully'
    }
    return JsonResponse(response_data)
