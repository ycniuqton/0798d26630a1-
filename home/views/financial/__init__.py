from datetime import datetime, timedelta, timezone

from django.http import Http404
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny

from config import APPConfig
from home.models import Vps, Invoice

from services.invoice import get_billing_cycle


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def payment_view(request):
    user = request.user
    balance = user.balance

    context = {
        'segment': 'payment',
        'balance': "{:,.2f}".format(balance.amount).replace(",", "."),
        'BANK_NAME': APPConfig.BANK_NAME,
        'BANK_ACCOUNT': APPConfig.BANK_ACCOUNT,
        'BANK_USERNAME': APPConfig.BANK_USERNAME,
    }
    return render(request, "pages/financial/payment.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resource_record(request):
    sample_data = [
        {
            "record_id": "Record 1",
            "location": "New York, USA",
            "configuration": "Config 1",
            "record_type": "Type A",
            "status": "Active",
            "record_time": "2024-07-10 14:30"
        },
        {
            "record_id": "Record 2",
            "location": "London, UK",
            "configuration": "Config 2",
            "record_type": "Type B",
            "status": "Inactive",
            "record_time": "2024-07-11 09:20"
        },
        {
            "record_id": "Record 3",
            "location": "Tokyo, Japan",
            "configuration": "Config 3",
            "record_type": "Type C",
            "status": "Active",
            "record_time": "2024-07-12 17:45"
        },
        {
            "record_id": "Record 4",
            "location": "Sydney, Australia",
            "configuration": "Config 4",
            "record_type": "Type D",
            "status": "Inactive",
            "record_time": "2024-07-13 12:15"
        },
        {
            "record_id": "Record 5",
            "location": "Berlin, Germany",
            "configuration": "Config 5",
            "record_type": "Type E",
            "status": "Active",
            "record_time": "2024-07-14 08:30"
        }
    ]

    context = {
        'segment': 'resource_record',
        'records': sample_data
    }
    return render(request, "pages/resource_record.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def billing_view(request):
    user = request.user
    if user.is_staff:
        invoices = Invoice.objects.all()
    else:
        invoices = Invoice.objects.filter(user_id=user.id).all()

    billing_records = {}
    for invoice in invoices:
        if invoice.cycle in billing_records:
            billing_records[invoice.cycle]['amount'] += invoice.amount
        else:
            billing_records[invoice.cycle] = {
                'amount': invoice.amount,
                'operation': 'View',
                'cycle': invoice.cycle
            }
    billing_records = list(billing_records.values())
    billing_records = sorted(billing_records, key=lambda x: x['cycle'], reverse=True)

    now = datetime.now(timezone.utc)
    this_cycle, _, _ = get_billing_cycle(now)
    last_hour_invoices = [i for i in invoices if i._created > now - timedelta(hours=1)]
    billing_summary = {
        "expenses": sum([i.amount for i in invoices]),
        "charges_this_month": sum([i.amount for i in invoices if i.cycle == this_cycle]),
        "charges_last_hour": sum([i.amount for i in last_hour_invoices]),
    }

    context = {
        'segment': 'billing',
        'billing_records': billing_records,
        'billing_summary': billing_summary
    }
    return render(request, "pages/financial/billing.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def financial_view(request):
    context = {
        'segment': 'financial'
    }
    return render(request, "pages/dynamic-tables.html", context)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def invoices_view(request):
    return render(request, 'pages/financial/invoices.html', {'segment': 'invoices'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    user = request.user
    balance = user.balance
    balance_records = balance.transactions.all()
    balance_records = [
        {
            "payment_account": record.user.email,
            "payment_type": record.type,
            "payment_method": record.method,
            "time": record._created,
            "recharge_amount": record.amount,
            "operation": "View"
        }
        for record in balance_records
    ]
    context = {
        'balance_records': balance_records,
    }

    return render(request, 'pages/financial/balance_record.html', context)


# @api_view(['GET'])
@permission_classes([AllowAny])
def invoice_view(request, invoice_id):
    invoice = Invoice.objects.filter(id=invoice_id).first()
    user = invoice.user
    if not invoice:
        Http404("Item does not exist")

    invoice_lines = invoice.lines.all()
    data = invoice.to_readable_dict()
    data['lines'] = [line.to_readable_dict() for line in invoice_lines]
    data['created'] = data['_created']
    context = {
        'invoice': data,
        'user': user.to_readable_dict()
    }

    return render(request, 'pages/financial/invoice_view.html', context)
