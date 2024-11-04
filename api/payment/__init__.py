import uuid

import requests
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
import json
from cryptomus import Client

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated

from adapters.paypal import PayPalClient
from config import PaypalConfig, APPConfig
from home.models import PaypalTransaction, User, BankTransaction
from services.balance import BalanceRepository
from utils import extract_url_params


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_url(request):
    payment_type = request.GET.get('type')
    amount = request.GET.get('amount')
    user = request.user

    # Mock receiver data
    receiver_info = {
        'paypal': {
            'payment_link': f'https://www.paypal.com/checkout?amount={amount}',
            'receiver_name': 'PayPal Receiver',
            'receiver_email': 'receiver@paypal.com'
        },
        'crypto': {
            'payment_link': f'https://www.crypto-payment.com/checkout?amount={amount}',
            'receiver_name': 'Crypto Wallet',
            'receiver_email': 'wallet@crypto.com'
        }
    }

    if payment_type == 'paypal':
        client = PayPalClient(
            mode=PaypalConfig.MODE,
            client_id=PaypalConfig.CLIENT_ID,
            client_secret=PaypalConfig.CLIENT_SECRET
        )
        payment_link, payment_id = client.generate_payment_link(total=amount, currency='USD',
                                                                description='Deposit to wallet',
                                                                return_url=PaypalConfig.RETURN_URL,
                                                                cancel_url=PaypalConfig.CANCEL_URL)
        # extract token
        params = extract_url_params(payment_link)

        payment_transaction = PaypalTransaction()
        payment_transaction.amount = amount
        payment_transaction.user = user
        payment_transaction.payment_id = payment_id
        payment_transaction.token = next(iter(params.get('token')), None)
        payment_transaction.save()

    elif payment_type == 'crypto':
        PAYMENT_KEY = APPConfig.CRYPTO_API_KEY
        MERCHANT_UUID = APPConfig.MERCHANT_ID

        payment_id = uuid.uuid4().hex

        client = Client.payment(PAYMENT_KEY, MERCHANT_UUID)

        payment_data = {
            'amount': amount,  # Amount in USD
            'currency': 'USD',
            'order_id': payment_id,
            'url_return': APPConfig.CRYPTO_RETURN_URL,
            'url_callback': APPConfig.CRYPTO_WEBHOOK_URL,
            'lifetime': '3600',  # Lifetime in seconds
        }

        # payment_transaction = PaypalTransaction()
        # payment_transaction.amount = amount
        # payment_transaction.user = user
        # payment_transaction.payment_id = payment_id
        # payment_transaction.save()

        response = client.create(payment_data)
        payment_link = response.get('url')

    else:
        payment_link = None

    return JsonResponse({'payment_link': payment_link, 'receiver_info': receiver_info.get(payment_type)})


# Mock exchange rate
EXCHANGE_RATE = 23000  # 1 USD = 23,000 VND


def paypal_success_callback(request):
    # get url params
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    p_transaction = PaypalTransaction.objects.filter(payment_id=payment_id).first()
    if not p_transaction:
        return JsonResponse({'error': 'Payment not found'}, status=404)

    client = PayPalClient(
        mode=PaypalConfig.MODE,
        client_id=PaypalConfig.CLIENT_ID,
        client_secret=PaypalConfig.CLIENT_SECRET
    )

    payment = client.verify_payment(payment_id, payer_id)
    if payment:
        try:
            paid_amount = float(payment.amount.total)
            currency = payment.amount.currency
        except:
            paid_amount = 0
            currency = None

        if paid_amount != p_transaction.amount:
            return JsonResponse({'error': 'Invalid payment amount or currency'}, status=400)

        p_transaction.status = PaypalTransaction.Status.PAID
        p_transaction.save()
        BalanceRepository().topup(p_transaction.user_id, p_transaction.amount)

        return HttpResponseRedirect('/payment/')

    return JsonResponse({'error': 'Payment verification failed'}, status=400)


def crypto_success_callback(request):
    print(request.body)
    print(request.headers)

    return JsonResponse({'message': 'Success'}, status=200)


def paypal_cancel_callback(request):
    token = request.GET.get('token')

    p_transaction = PaypalTransaction.objects.filter(token=token).first()
    if not p_transaction:
        return JsonResponse({'error': 'Payment not found'}, status=404)

    else:
        p_transaction.status = PaypalTransaction.Status.CANCELED
        p_transaction.save()

    return HttpResponseRedirect('/payment/')


@csrf_exempt
@permission_classes([AllowAny])
def crypto_webhook(request):
    # Mock payment success callback
    try:
        data = json.loads(request.body)
    except:
        data = []
    # get url params
    params = request.GET

    print("########### Webhook ###########")
    print(data)
    print(params)
    print(request.headers)

    # return the data
    return JsonResponse({'data': data, 'params': params}, status=200)


@csrf_exempt
@permission_classes([AllowAny])
def paypal_webhook(request):
    # Mock payment success callback
    try:
        data = json.loads(request.body)
    except:
        data = []
    # get url params
    params = request.GET

    print("########### Webhook ###########")
    print(data)
    print(params)
    print(request.headers)

    # return the data
    return JsonResponse({'data': data, 'params': params}, status=200)

    """
    ########### Webhook ###########
{'id': 'WH-7W152260D3445434F-4PN31168NS342104X', 'event_version': '1.0', 'create_time': '2024-09-18T00:22:51.301Z', 'resource_type': 'sale', 'event_type': 'PAYMENT.SALE.COMPLETED', 'summary': 'Payment completed for $ 111.0 USD', 'resource': {'amount': {'total': '111.00', 'currency': 'USD', 'details': {'subtotal': '111.00'}}, 'payment_mode': 'INSTANT_TRANSFER', 'create_time': '2024-09-18T00:22:46Z', 'transaction_fee': {'currency': 'USD', 'value': '4.36'}, 'parent_payment': 'PAYID-M3VB2RI2M010091F6141200L', 'update_time': '2024-09-18T00:22:46Z', 'soft_descriptor': 'PAYPAL *TEST STORE', 'protection_eligibility_type': 'ITEM_NOT_RECEIVED_ELIGIBLE,UNAUTHORIZED_PAYMENT_ELIGIBLE', 'application_context': {'related_qualifiers': [{'id': '4K685269UG814950X', 'type': 'CART'}]}, 'protection_eligibility': 'ELIGIBLE', 'links': [{'method': 'GET', 'rel': 'self', 'href': 'https://api.sandbox.paypal.com/v1/payments/sale/3G1015431R4987639'}, {'method': 'POST', 'rel': 'refund', 'href': 'https://api.sandbox.paypal.com/v1/payments/sale/3G1015431R4987639/refund'}, {'method': 'GET', 'rel': 'parent_payment', 'href': 'https://api.sandbox.paypal.com/v1/payments/payment/PAYID-M3VB2RI2M010091F6141200L'}], 'id': '3G1015431R4987639', 'state': 'completed', 'invoice_number': ''}, 'links': [{'href': 'https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-7W152260D3445434F-4PN31168NS342104X', 'rel': 'self', 'method': 'GET'}, {'href': 'https://api.sandbox.paypal.com/v1/notifications/webhooks-events/WH-7W152260D3445434F-4PN31168NS342104X/resend', 'rel': 'resend', 'method': 'POST'}]}
<QueryDict: {}>
{'Content-Length': '1499', 'Content-Type': 'application/json', 'Host': 'worldsever.com', 'X-Real-Ip': '173.0.80.117', 'X-Forwarded-For': '173.0.80.117', 'X-Forwarded-Proto': 'https', 'Connection': 'close', 'Accept': '*/*', 'Paypal-Transmission-Id': '2b703010-7554-11ef-9a64-85f88fc95a8f', 'Paypal-Transmission-Time': '2024-09-18T00:23:03Z', 'Paypal-Transmission-Sig': 'jE1oKkYm7qzo+SFAC4P6n+RteETwlafUo5ZlX/cI7y0otmdgBR6W28+4uUaEZvsKKwCKMnyB6uZCyaOMz1kUd1CwBkHnpnRzpDkctZ7lQiKDiAa9763noojOlRY4WIrqciTvgTcRVhlbHN0DY5Ibe/E4gwHyAvasLKzwBkMhWGH6oeC0FJ9xnwFF4S2lrWpvYiyp/4uiuU5onOiZhzX4UE2aOmHtrYrjm65oH3IVnY7dqMgWnolkyjRAzjW47dLyrGKqFucoHNE9ot08X/9s4T9UEUbp5aEAZhaKgShXpa/k6NtzEufowgeszjB4/O09hFXn/mAFQiV7hVqhZEawHg==', 'Paypal-Auth-Version': 'v2', 'Paypal-Cert-Url': 'https://api.sandbox.paypal.com/v1/notifications/certs/CERT-360caa42-fca2a594-ab66f33d', 'Paypal-Auth-Algo': 'SHA256withRSA', 'User-Agent': 'PayPal/AUHD-214.0-58644877', 'Correlation-Id': '73246b1ef1244', 'X-B3-Spanid': '1d94a651afa88003'}
    """


@csrf_exempt
@permission_classes([AllowAny])
def bank_webhook(request):
    # extract token from header  'Authorization': 'Bearer 988f06619fcc5f9e447041ef3fdcce450020838e0053a06128'
    token = request.headers.get('Authorization').split(' ')[1]
    if token != APPConfig.WEBHOOK_TOKEN:
        return JsonResponse({'error': 'Unauthorized'}, status=200)

    data = json.loads(request.body)
    transactions = data.get('transactions', [])

    for data in transactions:
        amount = data.get('transferAmount')
        amount = int(amount) / APPConfig.VND_USD_EXCHANGE_RATE
        payment_id = data.get('id')
        gateway = data.get('gateway')
        content = data.get('content')
        customer_code = content.split('UP ')[-1][:8].upper()
        payment_type = data.get('transferType')

        if payment_type != 'IN':
            continue

        # parse user
        user = User.objects.filter(customer_code=customer_code).first()
        if not user:
            user = User.objects.filter(username='system').first()

        duplicate_transaction = BankTransaction.objects.filter(payment_id=payment_id).first()
        if duplicate_transaction:
            continue

        BankTransaction.objects.create(
            user=user,
            amount=amount,
            payment_id=payment_id,
            gateway=gateway,
            description=content,
            raw_data=data,
            status=BankTransaction.Status.PENDING
        )
        if user:
            BalanceRepository().topup(user.id, amount)

    return JsonResponse({'message': 'Success'}, status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_qr_code(request):
    user = request.user
    amount = request.GET.get('amount', 0)
    amount = float(amount)
    vnd_amount = amount * APPConfig.VND_USD_EXCHANGE_RATE
    memo = f'UP {user.customer_code}'
    url = f'https://apiqr.web2m.com/api/generate/{APPConfig.BANK_NAME}/{APPConfig.BANK_ACCOUNT}/{APPConfig.BANK_USERNAME}?amount={vnd_amount}&memo={memo}'
    response = requests.get(url)
    if response.status_code != 200:
        return JsonResponse({'error': 'QR code generation failed'}, status=500)

    return HttpResponse(response.content, content_type=response.headers['Content-Type'], status=response.status_code)
