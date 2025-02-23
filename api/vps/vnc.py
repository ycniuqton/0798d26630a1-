import time
import json
import uuid
import requests
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from api.vps.__base__ import apply_vps_status
from core import settings
from home.models import Vps, VpsStatus, VNCSession
from django.http import JsonResponse
from adapters.redis_service import CachedPlan, CachedOS, CachedServer, CachedVpsStatRepository
from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig, VNCConfig
from services.invoice import InvoiceRepository
from services.vps import VPSService
from services.vps_log import VPSLogger
from services.balance import BalanceRepository
from django.utils import timezone


@extend_schema(
    request=dict,
    responses={200: dict},
    description="Get VNC link for a VPS instance",
    examples=[
        OpenApiExample(
            'Example Request',
            value={
                "vps_id": "your_vps_id"
            },
            request_only=True,
        ),
        OpenApiExample(
            'Example Response',
            value={
                "status": "success",
                "vnc_link": "https://example.com/vnc/session_key",
                "session_key": "session_key"
            },
            response_only=True,
        )
    ]
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_vnc_link(request, vps_id):
    user = request.user

    # Get VPS and verify ownership
    vps = get_object_or_404(Vps, id=vps_id)
    if not user.is_staff and vps.user_id != user.id:
        return JsonResponse({
            "status": "error",
            "message": "You don't have permission to access this VPS"
        }, status=403)

    # Check if VPS is in a valid state
    if vps.status not in [VpsStatus.ON]:
        return JsonResponse({
            "status": "error",
            "message": "VPS must be running to access VNC"
        }, status=400)

    # Check for existing non-expired VNC session
    vnc_session = VNCSession.objects.filter(vps=vps).first()
    
    if vnc_session:
        if vnc_session.is_expired():
            vnc_session.delete()
        else:
            # Return existing VNC session details
            return JsonResponse({
                "status": "success",
                "vnc_link": vnc_session.vnc_link,
                "session_key": vnc_session.session_key
            })
    
    # Generate new VNC session
    try:
        vps_service = VPSService(settings.VIRTUALIZOR_CONFIG.MANAGER_URL, settings.VIRTUALIZOR_CONFIG.API_KEY)
        vnc_info = vps_service.get_vnc(vps.linked_id)
        
        if not vnc_info:
            return JsonResponse({
                "status": "error",
                "message": "Failed to generate VNC session"
            }, status=500)
        
        # Generate session key and create VNC session
        session_key = str(uuid.uuid4())
        
        # Calculate expiration time
        expired_at = timezone.now() + timedelta(seconds=VNCConfig.SESSION_DURATION)
        
        # Create new VNC session
        vnc_session = VNCSession.objects.create(
            vps=vps,
            password=vnc_info.get('password'),
            port=vnc_info.get('port'),
            host=vnc_info.get('ip'),
            session_key=session_key,
            vnc_link=f"/vnc/{session_key}",
            expired_at=expired_at
        )
        
        return JsonResponse({
            "status": "success",
            "vnc_link": vnc_session.vnc_link,
            "session_key": vnc_session.session_key
        })
            
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": f"Error generating VNC session: {str(e)}"
        }, status=500)
