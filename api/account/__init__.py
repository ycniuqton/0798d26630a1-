from functools import reduce

from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from home.models import Vps
from django.http import JsonResponse, HttpResponse


class AccountAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = {
            'email': 'ngohongqui@gmail.com',
            'first_name': 'Ngô',
            'last_name': 'Quí',
            'address': 'Số 60 ngách 52/25 phú mỹ mỹ đình từ liêm hà nội',
            'city': 'Hà Nội',
            'country_region': 'Hong Kong (China)',
            'zip_code': '100000',
            'company_name': '',
            'phone_country': 'Vietnam(84)',
            'phone_number': '365046569',
            'subscribe_email': True
        }
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
