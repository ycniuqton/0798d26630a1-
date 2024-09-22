import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from home.models import Vps, User
from django.http import JsonResponse, HttpResponse
from services.balance import BalanceRepository


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def topup(request):
    data = json.loads(request.body)
    user = request.user
    amount = data.get('amount', 0)

    if not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    acc = User.objects.filter(email=data.get('email')).first()

    if not amount or not acc:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    BalanceRepository().topup(acc.id, amount)

    publisher = make_kafka_publisher(KafkaConfig)
    publisher.publish('balance_topped_up', {
        'user_id': acc.id})

    return JsonResponse({'message': 'Topup success'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reclaim(request):
    data = json.loads(request.body)
    user = request.user
    amount = data.get('amount', 0)

    if not user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    acc = User.objects.filter(email=data.get('email')).first()

    if not amount or not acc:
        return JsonResponse({'error': 'Invalid request'}, status=400)

    BalanceRepository().reclaim(acc.id, amount)

    return JsonResponse({'message': 'Topup success'})
