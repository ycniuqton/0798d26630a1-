from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from home.models import Vps


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
