import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan, CachedServer, CachedOS
from home.models import Vps

from django.http import JsonResponse


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vps_calculator(request):
    data = json.loads(request.body)

    serid = data.get('location', {}).get('id', 0)
    plid = data.get('plan', {}).get('id', 0)
    # image_version = data.get('image', {}).get('version', 'None')
    duration = data.get('duration', 1)

    osid = None
    plans = CachedPlan().get()
    # servers = CachedServer().get()
    # oses = CachedOS().get()
    # for os in oses:
    #     if os['name'] == image_version:
    #         osid = os['id']
    #         break
    try:
        plan = [plan for plan in plans if plan['id'] == int(plid)][0]
    except:
        plan = None

    # try:
    #     server = [server for server in servers if server['id'] == int(serid)][0]
    # except:
    #     server = None

    if not plan:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    total_fee = plan['price'] * duration

    return JsonResponse({'total_cost': total_fee})
