from functools import reduce

from django.core.paginator import Paginator
from django.http import JsonResponse
from home.models import VPSLog
from django.db.models import Q


def get_vps_logs(request):
    user = request.user

    filterable_fields = ['hostname', 'action', 'status', 'user__username', 'vps_id']
    search_fields = ['hostname', 'action', 'status', 'performed_by']
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    sort_by = request.GET.get('sort_by', '-datetime')
    filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
    search_value = request.GET.get('search')
    search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                    ]
    if search_query:
        search_query = reduce(lambda x, y: x | y, search_query)
    else:
        search_query = Q()

    logs = VPSLog.objects.filter(**filters).filter(search_query)
    if not user.is_staff:
        logs = logs.filter(user_id=user.id)

    total = logs.count()

    logs = logs.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

    logs_data = [data.to_readable_dict() for data in logs]

    return JsonResponse({
        'logs': logs_data,
        'total_pages': (total - 1) // page_size + 1,
        'current_page': page,
        'has_next': total > page * page_size,
        'has_previous': page > 1,
    })
