from django.shortcuts import render, redirect
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta, date
from django.shortcuts import render
from django.core.paginator import Paginator
import random
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from services.vps import VPSService
from home.models import Vps, VPSLog

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
import os
from .detail import *

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_customer(request):
    user = request.user
    list_email = []
    if user.is_staff:
        customers = User.objects.filter(is_staff=False)
        list_email = [customer.email for customer in customers]

    context = {
        'list_email': list_email
    }
    return render(request, 'pages/customers/page.html', context)
