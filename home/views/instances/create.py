from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan, CachedOS, CachedServer, CachedServerGroup, CachedPlanInRegion
from utils import country_mapping, country_short_to_region


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_instances(request):
    plans = CachedPlan().get()
    # plans = [
    #     {
    #         "name": "VPS VN-1",
    #         "vcpu": "1 vCPU",
    #         "ram": "1GB RAM",
    #         "bandwidth": "1TB băng thông",
    #         "storage": "20GB SSD Enterprise",
    #         "price": "60,000 đ",
    #         "backup": "NO BACKUP",
    #         "link": "#"
    #     }
    # ]
    ipv4_options = ["1 IPv4", "2 IPv4", "5 IPv4"]
    bandwidth_options = ["Default", "+ 5TB", "+ 10TB"]
    ram_options = ["Default", "+ 3GB", "+ 6GB"]
    ssd_options = ["Default", "+ 50GB", "+ 100GB"]

    # country
    regions = [
        {"name": "Asia", "status": "on"},
        {"name": "North America", "status": "on"},
        {"name": "Europe", "status": "on"},
        {"name": "South America", "status": "on"},
        {"name": "Africa", "status": "on"},
        {"name": "Oceania", "status": "on"},
        {"name": "Middle East", "status": "on"},
        {"name": "ALL", "status": "on"}
    ]

    servers = CachedServer().get()
    server_groups = CachedServerGroup().get()
    locations = [
        {"name": "Washington", "country": "USA", "region": "North America", "status": "off", "country_short": "US"},
        {"name": "Silicon Valley", "country": "USA", "region": "North America", "status": "off", "country_short": "US"},
        {"name": "Toronto", "country": "Canada", "region": "North America", "status": "off", "country_short": "CA"},
        {"name": "Vancouver", "country": "Canada", "region": "North America", "status": "off", "country_short": "CA"},
        {"name": "Frankfurt", "country": "Germany", "region": "Europe", "status": "off", "country_short": "DE"},
        # {"name": "London", "country": "UK", "region": "Europe", "status": "off", "country_short": "GB"},
        # {"name": "Paris", "country": "France", "region": "Europe", "status": "off", "country_short": "FR"},
        # {"name": "Amsterdam", "country": "Netherlands", "region": "Europe", "status": "off", "country_short": "NL"},
        # {"name": "Jakarta", "country": "Indonesia", "region": "Asia", "status": "off", "country_short": "ID"},
        # {"name": "HoChiMinh", "country": "VietNam", "region": "Asia", "status": "off", "country_short": "VN"},
        # {"name": "Singapore", "country": "Singapore", "region": "Asia", "status": "off", "country_short": "SG"},
        # {"name": "Tokyo", "country": "Japan", "region": "Asia", "status": "off", "country_short": "JP"},
        # {"name": "Seoul", "country": "South Korea", "region": "Asia", "status": "off", "country_short": "KR"},
        # {"name": "São Paulo", "country": "Brazil", "region": "South America", "status": "off", "country_short": "BR"},
        # {"name": "Buenos Aires", "country": "Argentina", "region": "South America", "status": "off",
        #  "country_short": "AR"},
        # {"name": "Cape Town", "country": "South Africa", "region": "Africa", "status": "off", "country_short": "ZA"},
        # {"name": "Nairobi", "country": "Kenya", "region": "Africa", "status": "off", "country_short": "KE"},
        # {"name": "Sydney", "country": "Australia", "region": "Oceania", "status": "off", "country_short": "AU"},
        # {"name": "Melbourne", "country": "Australia", "region": "Oceania", "status": "off", "country_short": "AU"},
        # {"name": "Dubai", "country": "UAE", "region": "Middle East", "status": "off", "country_short": "AE"},
        # {"name": "Riyadh", "country": "Saudi Arabia", "region": "Middle East", "status": "off", "country_short": "SA"}
    ]
    mapping_region_plans = {}
    for sg in server_groups:
        group_id = sg.get("id")
        locations.append({
            "name": sg.get("name"),
            "country": country_mapping.get(sg.get("country").upper()),
            "region": country_short_to_region.get(sg.get("country").upper()),
            "status": "on",
            "country_short": sg.get("country").upper(),
            "group_id": group_id,
            "cluster_id": sg.get("cluster_id")
        })
        list_plan = CachedPlanInRegion().get(group_id) if CachedPlanInRegion().get(
            group_id) else []
        mapping_region_plans[group_id] = list_plan

    locations = sorted(locations, key=lambda x: (x['status'], x.get('cluster_id'), x.get('id')), reverse=True)

    # Fetch flags using restcountries.com API
    # for location in locations:
    #     response = requests.get(f"https://restcountries.com/v3.1/name/{location['country']}?fields=flags")
    #     if response.status_code == 200:
    #         location_data = response.json()
    #         if location_data:
    #             location['flag'] = location_data[0]['flags']['png']
    #     else:
    #         location['flag'] = "https://via.placeholder.com/30"  # Fallback image

    # OS
    categories = ["ALL", "System Image"]
    categories = ["ALL"]
    oses = CachedOS().get()
    oses_dict = {}
    for os in oses:
        distro = os.get("distro")
        if distro not in oses_dict:
            oses_dict[distro] = {
                "name": distro,
                "versions": [{"name": os.get("name"), "cluster_id": os.get("cluster_id")}],
                "category": "System Image",
                "image_url": distro.lower() + ".png"
            }
        else:
            oses_dict[distro]["versions"].append({"name": os.get("name"), "cluster_id": os.get("cluster_id")})

    images = list(oses_dict.values())
    for image in images:
        list_of_cluster_ids = [version["cluster_id"] for version in image["versions"]]
        image["cluster_hash"] = "".join(set([f":{cluster_id}:" for cluster_id in list_of_cluster_ids]))

        # images = [
        #     {"name": "Ubuntu", "versions": ["18.04", "19.04", "20.04", "22.04"], "category": "System Image",
        #      "image_url": "ubuntu.png"},
        #     {"name": "Debian", "versions": ["9", "10", "11"], "category": "System Image",
        #      "image_url": "debian.png"},
        #     {"name": "AlmaLinux", "versions": ["8.4", "8.5", "8.6"], "category": "System Image",
        #      "image_url": "almalinux.png"},
        #     {"name": "CentOS", "versions": ["7", "8"], "category": "System Image",
        #      "image_url": "centos.png"},
        #     {"name": "FreeBSD", "versions": ["11", "12", "13"], "category": "System Image",
        #      "image_url": "freebsd.png"},
        #     {"name": "Rocky Linux", "versions": ["8.4", "8.5", "8.6"], "category": "System Image",
        #      "image_url": "rockylinux.png"},
        #     {"name": "Windows", "versions": ["10", "Server 2016", "Server 2019"], "category": "System Image",
        #      "image_url": "windows.png"},
        # ]

    context = {
        'segment': 'create_instances',
        'plans': plans,
        # 'ipv4_options': ipv4_options,
        # 'bandwidth_options': bandwidth_options,
        # 'ram_options': ram_options,
        # 'ssd_options': ssd_options,
        'regions': regions,
        'locations': locations,
        'categories': categories,
        'images': images,
        'mapping_region_plans': mapping_region_plans,
    }
    return render(request, "pages/instances/create/create-instances.html", context)
