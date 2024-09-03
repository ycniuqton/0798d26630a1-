import json
from datetime import datetime
from functools import reduce

from admin_datta.utils import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from home.models import Ticket


class TicketCollectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = json.loads(request.body)
            ticket = Ticket.objects.create(
                subject=data['subject'],
                ticket_type=data['ticket_type'],
                description=data['description'],
                submission_time=datetime.now(),
                status='open',
                operation='View',
                user=request.user
            )
            ticket = ticket.to_readable_dict()
            return JsonResponse({'success': True, 'ticket': ticket})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    def get(self, request):
        user = request.user

        filterable_fields = ['subject', 'ticket_type', 'description', 'status', 'user__username']
        search_fields = ['subject', 'ticket_type', 'description', 'status', 'user__username']
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        page_size = 5
        sort_by = request.GET.get('sort_by', '-datetime')
        filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
        search_value = request.GET.get('search')
        search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                        ]
        if search_query:
            search_query = reduce(lambda x, y: x | y, search_query)
        else:
            search_query = Q()

        logs = Ticket.objects.filter(**filters).filter(search_query)
        if not user.is_staff:
            logs = logs.filter(user_id=user.id)

        total = logs.count()

        objects = logs.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        data = []
        for obj in objects:
            obj_data = obj.to_readable_dict()
            obj_data.update({'messages': [msg.to_readable_dict() for msg in obj.messages.all()]})
            data.append(obj_data)

        return JsonResponse({
            'tickets': data,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })


class TicketAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, ticket_id):
        user = request.user

        ticket = Ticket.objects.filter(id=ticket_id)
        if not user.is_staff:
            ticket = ticket.filter(user_id=user.id)
        ticket = ticket.first()
        ticket = ticket.to_readable_dict()

        return JsonResponse(ticket)