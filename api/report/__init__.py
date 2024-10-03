import requests
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated

from adapters.paypal import PayPalClient
from config import PaypalConfig, APPConfig
from home.models import PaypalTransaction, User, BankTransaction
from services.balance import BalanceRepository
from utils import extract_url_params


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dashboard_statistic(request):
    user = request.user
    if not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    total_users = User.objects.count()
    total_vps = Vps.objects.count()
    total_vps_active = Vps.objects.filter(status=VpsStatus.ACTIVE).count()
    total_vps_suspended = Vps.objects.filter(status=VpsStatus.SUSPENDED).count()
    total_vps_deleted = Vps.objects.filter(status=VpsStatus.DELETED).count()
    total_vps_pending = Vps.objects.filter(status=VpsStatus.PENDING).count()
    total_vps_rebuilding = Vps.objects.filter(status=VpsStatus.REBUILDING).count()

    return JsonResponse({
        'total_users': total_users,
        'total_vps': total_vps,
        'total_vps_active': total_vps_active,
        'total_vps_suspended': total_vps_suspended,
        'total_vps_deleted': total_vps_deleted,
        'total_vps_pending': total_vps_pending,
        'total_vps_rebuilding': total_vps_rebuilding,
    })
