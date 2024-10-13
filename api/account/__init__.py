from functools import reduce

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import Vps, User
from django.http import JsonResponse, HttpResponse
from .token import *


class AccountAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user = user.to_readable_dict()
        return JsonResponse(user)

    def put(self, request):
        data = request.data
        user = request.user
        updatable_fields = ['first_name', 'last_name', 'address', 'city', 'country_region', 'zip_code', 'company_name',
                            'phone_country', 'phone_number', 'subscribe_email']
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        user.save()
        return JsonResponse(user.to_readable_dict())


class AccountBalanceAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            balance = user.balance
            balance = balance.to_readable_dict()
        except:
            balance = {}
        return JsonResponse(balance)


class AccountCollectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Invalid request'}, status=400)

        filterable_fields = []
        search_fields = []
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

        list_user = User.objects.filter(is_staff=False).filter(**filters).filter(search_query)

        total = list_user.count()

        list_user = list_user.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        list_user = [data.to_readable_dict() for data in list_user]

        ignored_fields = ['password']
        for acc in list_user:
            for field in ignored_fields:
                try:
                    acc.pop(field, None)
                except:
                    pass

        return JsonResponse({
            'logs': list_user,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })
