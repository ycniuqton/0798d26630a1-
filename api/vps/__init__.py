from functools import reduce

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import Vps
from django.http import JsonResponse, HttpResponse


class VPSAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        filterable_fields = ['hostname', 'location', 'ip_address', 'status']
        search_fields = ['hostname', 'location', 'ip_address', 'status']
        sortable_fields = ['hostname', 'location', 'ip_address', 'status', '_created']
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        sort_by = request.GET.get('sort_by', '-_created')
        sort_by = sort_by if sort_by in sortable_fields else '-_created'
        filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
        search_value = request.GET.get('search')
        search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                        ]
        if search_query:
            search_query = reduce(lambda x, y: x | y, search_query)
        else:
            search_query = Q()

        objects = Vps.objects.filter(**filters).filter(search_query)
        total = objects.count()

        objects = objects.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        data = [data.to_readable_dict() for data in objects]

        return JsonResponse({
            'data': data,
            'total_pages': (total-1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })
