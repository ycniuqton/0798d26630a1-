from django.shortcuts import render
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from adapters.redis_service import CachedPlan, CachedOS
from home.models import Vps, User


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_detail(request, customer_id):
    user = request.user
    customer = User.objects.filter(id=customer_id)
    if not user.is_staff:
        customer = customer.filter(user_id=user.id)

    customer = customer.first()

    context = {
        'customer': customer,
        'instance': 'VPS'
    }

    return render(request, 'pages/customers/detail.html', context)
