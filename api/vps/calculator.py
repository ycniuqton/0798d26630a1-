import time
import json
from datetime import datetime, timedelta
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan, CachedServer, CachedOS
from home.models import Vps

from django.http import JsonResponse

from services.discount import DiscountRepository
from services.purchase_estimator import PurchaseEstimator


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vps_calculator(request):
    data = json.loads(request.body)

    serid = data.get('location', {}).get('id', 0)
    plid = data.get('plan', {}).get('id', 0)
    image_version = data.get('image', {}).get('version', 'None')
    duration = data.get('duration', 1)

    osid = None
    plans = CachedPlan().get()
    # servers = CachedServer().get()
    oses = CachedOS().get()
    for os in oses:
        if os['name'] == image_version:
            osid = os['id']
            break
    try:
        plan = [plan for plan in plans if plan['id'] == int(plid)][0]
    except:
        plan = None

    if not plan or os.get('id') != osid:
        return JsonResponse({
            'message': 'Please select a plan and os.',
            'is_valid': False
        }, status=200)
    purchase_estimator = PurchaseEstimator(request.user)
    is_valid, message, discounted_fee, discount_amount, total_fee = purchase_estimator.estimate(plan, os, duration)

    return JsonResponse({
        'discount_percent': purchase_estimator.discount_repo.discount_percent,
        'is_valid': is_valid,
        'message': message,
        'discounted_fee': discounted_fee,
        'discount_amount': discount_amount,
        'total_fee': total_fee
    }, status=200)
