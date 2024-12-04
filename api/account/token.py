import json
import uuid
from functools import reduce

from django.db.models import Q
from django.utils import timezone

from admin_datta.utils import JsonResponse
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import UserToken
from services.account import UserTokenRepository
from services.invoice import get_now


class UserTokenAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        tokens = UserToken.objects.filter()
        if not user.is_staff:
            tokens = tokens.filter(user_id=user.id)
        tokens = tokens.all()
        result = []
        for token in tokens:
            token_data = token.to_readable_dict()
            if token.expired_at < timezone.now() and token.ttl != -1:
                token_data['status'] = 'Expired'
            else:
                token_data['status'] = 'Active'
            if token.ttl == -1:
                token_data['expired_at'] = 'Never'
            result.append(token_data)

        return JsonResponse(result, safe=False)

    def get(self, request):
        user = request.user

        filterable_fields = ['user__username']
        search_fields = ['user__username']
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        sort_by = request.GET.get('sort_by', '-_created')
        filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
        search_value = request.GET.get('search')
        search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                        ]
        if search_query:
            search_query = reduce(lambda x, y: x | y, search_query)
        else:
            search_query = Q()

        logs = UserToken.objects.filter(**filters).filter(search_query)
        if not user.is_staff:
            logs = logs.filter(user_id=user.id)

        total = logs.count()

        logs = logs.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        logs_data = []
        now = get_now()
        for data in logs:
            token = data.to_readable_dict()
            if data.expired_at < now and data.ttl != -1:
                token['status'] = 'Expired'
            else:
                token['status'] = 'Active'
            if data.ttl == -1:
                token['expired_at'] = 'Never'
            logs_data.append(token)

        return JsonResponse({
            'data': logs_data,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })

    def post(self, request):
        user = request.user
        data = json.loads(request.body)
        ttl = int(data.get('ttl', 3600))

        token = UserTokenRepository().create_token(user_id=user.id,
                                                   ttl=ttl,
                                                   description=data.get('description', ''))
        expired_at = token.expired_at
        token = token.to_readable_dict()
        if expired_at < timezone.now() and ttl != -1:
            token['status'] = 'Expired'
        else:
            token['status'] = 'Active'
        return JsonResponse(token)


@permission_classes([IsAuthenticated])
def delete_token(request, token_id):
    user = request.user
    token = UserToken.objects.filter(id=token_id)
    if not user.is_staff:
        token = token.filter(user_id=user.id)
    token = token.first()
    if not token:
        return JsonResponse({'success': False, 'error': 'Token not found'}, status=400)
    UserTokenRepository().delete_token(token.id)
    return JsonResponse({'success': True})
