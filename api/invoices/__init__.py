import json
from functools import reduce

from django.db.models import Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from home.models import Vps, Invoice, Transaction
from django.http import JsonResponse, HttpResponse
from services.balance import BalanceRepository


class InvoiceCollectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        filterable_fields = ['code', '_created', 'status', 'amount', 'user__username', 'user_id']
        search_fields = ['code', '_created', 'status', 'amount', 'user__username']
        sortable_fields = ['code', '_created', 'status', 'amount']
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        sort_by = request.GET.get('sort_by', '-_created')
        sort_by = sort_by if sort_by in sortable_fields else '-_created'
        filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
        search_value = request.GET.get('search')
        search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                        ]
        if search_query:
            search_query = reduce(lambda x, y: x | y, search_query)
        else:
            search_query = Q()

        objects = Invoice.objects.filter(**filters).filter(search_query)
        if not user.is_staff:
            objects = objects.filter(user_id=user.id)
        total = objects.count()

        objects = objects.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        data = [data.to_readable_dict() for data in objects]

        return JsonResponse({
            'data': data,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1,
        })

    def post(self, request):
        user = request.user
        if not user.is_staff:
            return JsonResponse({'error': 'Permission denied'}, status=403)

        data = json.loads(request.body)
        due_date = data.get('due_date')
        invoice_id = data.get('id')

        invoice = Invoice.objects.get(id=invoice_id)
        if not invoice:
            return JsonResponse({'error': 'Invoice not found'}, status=404)

        invoice.due_date = due_date
        invoice.save()

        return JsonResponse({'message': 'Invoice updated successfully'}, status=200)


class InvoiceAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_id):
        user = request.user
        invoice = Invoice.objects.filter(id=invoice_id)
        if not user.is_staff:
            invoice = invoice.filter(user_id=user.id)
        invoice = invoice.first()

        if not invoice:
            return JsonResponse({'error': 'Invoice not found'}, status=404)

        invoice_lines = invoice.lines.all()
        data = invoice.to_readable_dict()
        data['lines'] = [il.to_readable_dict() for il in invoice_lines]

        return JsonResponse(data)


class TransactionCollectionAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        filterable_fields = ['user__username', 'user_id']
        search_fields = ['user__username']
        sortable_fields = []
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        sort_by = request.GET.get('sort_by', '-_created')
        sort_by = sort_by if sort_by in sortable_fields else '-_created'
        filters = {field: request.GET.get(field) for field in filterable_fields if request.GET.get(field)}
        search_value = request.GET.get('search')
        search_query = [Q(**{f'{field}__icontains': search_value}) for field in search_fields if search_value
                        ]
        if search_query:
            search_query = reduce(lambda x, y: x | y, search_query)
        else:
            search_query = Q()

        objects = Transaction.objects.filter(**filters).filter(search_query)
        if not user.is_staff:
            objects = objects.filter(user_id=user.id)
        total = objects.count()

        objects = objects.order_by(sort_by).all()[page_size * (page - 1):page_size * page]

        data = []
        for obj in objects:
            obj_data = obj.to_readable_dict()
            obj_data['created'] = obj._created
            data.append(obj_data)

        return JsonResponse({
            'data': data,
            'total_pages': (total - 1) // page_size + 1,
            'current_page': page,
            'has_next': total > page * page_size,
            'has_previous': page > 1
        })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def charge_invoice(request, invoice_id):
    user = request.user
    invoice = Invoice.objects.filter(id=invoice_id)
    if not user.is_staff:
        invoice = invoice.filter(user_id=user.id)
    invoice = invoice.first()

    if not invoice:
        return JsonResponse({'error': 'Invoice not found'}, status=404)

    publisher = make_kafka_publisher(KafkaConfig)
    publisher.publish('charge_invoice', payload={
        'invoice_id': invoice.id
    })

    return JsonResponse({'message': 'Invoice paid successfully'}, status=200)
