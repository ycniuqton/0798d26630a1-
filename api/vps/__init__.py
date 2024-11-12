from functools import reduce

from django.db.models import Q
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import Vps
from django.http import JsonResponse, HttpResponse
from .start import start_vps
from .stop import stop_vps
from .restart import restart_vps
from .suspend import suspend_vps
from .un_suspend import unsuspend_vps
from .give import give_vps
from .change_plan import change_vps_plan
from .update_info import update_info


class VPSAPI(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,  # No request body for GET method
        responses={200: dict},  # Adjust response schema as needed
        description="Retrieve a list of VPS instances with optional filtering, sorting, and pagination.",
        parameters=[
            OpenApiParameter(
                name="page",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Page number for pagination",
                required=False
            ),
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Number of items per page",
                required=False
            ),
            OpenApiParameter(
                name="sort_by",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Field to sort by (e.g., 'name' or '-created')",
                required=False
            ),
            OpenApiParameter(
                name="search",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Search term to filter results",
                required=False
            ),
        ],
        examples=[
            OpenApiExample(
                'Example Request with Pagination',
                value={"page": 1, "page_size": 10},
                request_only=True,  # Applies to the request only
            ),
            OpenApiExample(
                'Example Response',
                value={
                    "count": 100,
                    "page": 1,
                    "page_size": 10,
                    "results": [
                        {"id": "vps123", "name": "VPS Instance 1"},
                        {"id": "vps124", "name": "VPS Instance 2"},
                        # more results...
                    ]
                },
                response_only=True,  # Applies to the response only
            )
        ]
    )
    def get(self, request):
        user = request.user
        filterable_fields = ['hostname', 'location', 'ip', 'status', 'user__username', 'user_id']
        search_fields = ['hostname', 'location', 'ip', 'status', 'user__username']
        sortable_fields = ['hostname', 'location', 'ip', 'status', '_created']
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

        objects = Vps.objects.filter(~Q(_deleted=True)).filter(**filters).filter(search_query)
        if not user.is_staff:
            objects = objects.filter(user_id=user.id)
        total = objects.count()

        objects = objects.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        data = [data.to_readable_dict() for data in objects]

        # exclude some fields from the response
        for item in data:
            region = item.get('region', {})
            if isinstance(region, dict):
                region.pop('server', None)
            item.pop('password', None)

        return JsonResponse({
            'data': data,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })
