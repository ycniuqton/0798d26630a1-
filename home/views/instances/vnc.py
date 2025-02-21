from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from config import VNCConfig
from home.models import VNCSession


@login_required
def vnc_view(request, session_key):
    # Get VNC session
    vnc_session = VNCSession.objects.filter(session_key=session_key).first()
    if not vnc_session:
        return render(request, 'pages/common/404.html', {'message': 'VNC session not found'})

    # Check if session is expired
    if vnc_session.is_expired():
        vnc_session.delete()  # Clean up expired session
        return render(request, 'pages/common/404.html', {'message': 'VNC session has expired. Please request a new session.'})

    # Check if user has access to this VPS
    if not request.user.is_staff and vnc_session.vps.user_id != request.user.id:
        return render(request, 'pages/common/404.html', {'message': 'Access denied'})

    context = {
        'host': VNCConfig.DOMAIN_URL,
        'port': VNCConfig.PORT,
        'password': vnc_session.password,
        'session_key': vnc_session.session_key,
    }
    return render(request, 'vnc/vnc_lite.html', context)
