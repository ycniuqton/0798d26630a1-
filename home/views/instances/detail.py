from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan, CachedOS, CachedVpsStatRepository
from home.models import Vps


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instance_detail(request, instance_id):
    user = request.user
    vps = Vps.objects.filter(id=instance_id)
    if not user.is_staff:
        vps = vps.filter(user_id=user.id)

    vps = vps.first()
    region = vps.region
    cluster_id = region.get('cluster_id')

    plans = CachedPlan().get()
    if not vps:
        instance = {
            'id': 123,
            'server_name': 'Server-01',
            'ip_address': '192.168.1.1',
            'location': 'New York',
            'os': 'Ubuntu 20.04 LTS',
            'created_at': '2024-07-20 12:34:56',
            'last_modified': '2024-07-20 12:34:56',
            'detailed_location': 'Seoul',
            'country': 'South Korea',
            'image': 'AlmaLinux 8.4',
            'instance_type': 'VPS VN-3',
            'vcpu': '2 vCPU',
            'ram': '2GB RAM',
            'network': '3TB băng thông',
            'storage': '20GB SSD Enterprise',
            'additional_ipv4': '1 IPv4',
            'additional_ram': '+ 3GB',
            'additional_ssd': '+ 50GB',
            'bandwidth': '',
            'hostname': '2024071001535329714',
            'login': 'root',
            'password': 'password123'
        }
    else:
        instance = vps
        instance.created = vps._created
        instance.updated = vps._updated
        instance.deleted = vps._deleted

        try:
            instance.plan_name = [i['name'] for i in plans if i['id'] == vps.plan_id][0]
        except:
            instance.plan_name = ""
    oses = CachedOS().get()
    oses_dict = {}
    for os in oses:
        if os.get("cluster_id") != cluster_id:
            continue
        distro = os.get("distro")
        if distro not in oses_dict:
            oses_dict[distro] = {
                "name": distro,
                "versions": [os.get("name")],
                "category": "System Image",
                "image_url": distro.lower() + ".png"
            }
        else:
            oses_dict[distro]["versions"].append(os.get("name"))

    images = list(oses_dict.values())

    instance_types = plans

    cvr = CachedVpsStatRepository()
    if instance.linked_id:
        stats = cvr.get(instance.linked_id)
    else:
        stats = {
            "bandwidth": "0",
            "disk": "0",
            "inode": 0,
            "io_read": 0,
            "io_write": 0,
            "lock_status": False,
            "net_in": "0",
            "net_out": "0",
            "network_status": False,
            "ram": "0",
            "status": 0,
            "used_bandwidth": "0",
            "used_cpu": "0",
            "used_disk": 0,
            "used_inode": "0",
            "used_ram": 0,
            "virt": "kvm"
        }

    context = {
        'instance': instance,
        'images': images,
        'instance_types': instance_types,
        'stats': stats,
    }

    return render(request, 'pages/instances/detail.html', context)
