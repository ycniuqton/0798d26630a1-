from django.shortcuts import render


def ctv_financial(request):
    user = request.user
    balance = user.balance
    balance_records = balance.transactions.all()
    balance_records = [
        {
            "payment_account": record.user.email,
            "payment_type": record.type,
            "payment_method": "System",
            "time": record._created,
            "recharge_amount": record.amount,
            "operation": "View"
        }
        for record in balance_records
    ]
    context = {
        'segment': 'payment',
        'balance_records': balance_records,
        'balance': balance.amount
    }
    return render(request, "pages/ctv-admin/financial.html", context)


def ctv_settings(request):
    user = request.user
    balance = user.balance
    balance_records = balance.transactions.all()
    balance_records = [
        {
            "payment_account": record.user.email,
            "payment_type": record.type,
            "payment_method": "System",
            "time": record._created,
            "recharge_amount": record.amount,
            "operation": "View"
        }
        for record in balance_records
    ]
    context = {
        'segment': 'payment',
        'balance_records': balance_records,
        'balance': balance.amount
    }
    return render(request, "pages/ctv-admin/settings.html", context)


def admin_invoices(request):
    return render(request, "pages/ctv-admin/invoices.html", context={})


def refund_requests(request):
    return render(request, "pages/ctv-admin/refund_requests.html", context={})

