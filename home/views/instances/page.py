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
from home.models import Vps

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
import os


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def instances(request):
    user = request.user
    instances_data = []
    list_user = []

    if user.is_staff:
        list_user = Vps.objects.values('user__username').distinct()
        list_user = [user['user__username'] for user in list_user]

    context = {
        'segment': 'instances',
        'instances': instances_data,
        'list_user': list_user
    }
    return render(request, "pages/instances/instances.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def archived_instances(request):
    user = request.user
    instances_data = []
    list_user = []

    if user.is_staff:
        list_user = Vps.objects.values('user__username').distinct()
        list_user = [user['user__username'] for user in list_user]

    context = {
        'segment': 'instances',
        'instances': instances_data,
        'list_user': list_user
    }
    return render(request, "pages/instances/archived_instances.html", context)
