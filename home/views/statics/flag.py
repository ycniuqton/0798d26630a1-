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

from services.vps import VPSService
from home.models import Vps

from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views import View
import os


class FlagAPI(View):
    def get(self, request, country_code):
        # Define the path to the flag
        flag_path = os.path.join(settings.STATICFILES_DIRS[0], 'assets', 'country_flags', '4x3', f'{country_code}.svg')

        # Check if the flag exists
        if os.path.exists(flag_path):
            with open(flag_path, 'rb') as f:
                return HttpResponse(f.read(), content_type="image/svg+xml")
        else:
            return JsonResponse({'error': 'Flag not found'}, status=404)
