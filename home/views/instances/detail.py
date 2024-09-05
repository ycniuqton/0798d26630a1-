from django.shortcuts import render

from adapters.redis_service import CachedPlan, CachedOS
from home.models import Vps


def instance_detail(request, instance_id):
    user = request.user
    vps = Vps.objects.filter(id=instance_id)
    if not user.is_staff:
        vps = vps.filter(user_id=user.id)

    vps = vps.first()

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

        try:
            instance.plan_name = [i['name'] for i in plans if i['id'] == vps.plan_id][0]
        except:
            instance.plan_name = ""

    oses = CachedOS().get()
    oses_dict = {}
    for os in oses:
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

    context = {
        'instance': instance,
        'images': images,
        'instance_types': instance_types,
    }

    return render(request, 'pages/instances/detail.html', context)
