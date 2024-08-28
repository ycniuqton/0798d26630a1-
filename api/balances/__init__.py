import json
from functools import reduce

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import Vps
from django.http import JsonResponse, HttpResponse
from services.balance import BalanceRepository


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def topup(request):
    data = json.loads(request.body)
    user = request.user
    amount = data.get('amount', 0)

    if not amount:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    BalanceRepository().topup(user.id, amount)

    return JsonResponse({'message': 'Topup success'})
