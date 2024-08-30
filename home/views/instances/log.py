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


def vps_history(request):
    user = request.user
    list_user = []

    if user.is_staff:
        list_user = VPSLog.objects.values('user__username').distinct()
        list_user = [user['user__username'] for user in list_user]

    context = {
        'list_user': list_user,
        'logs': []
    }
    return render(request, 'pages/instances/history/history.html', context)
