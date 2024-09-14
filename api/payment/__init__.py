from django.http import JsonResponse
from django.http import HttpResponseRedirect
import json

from adapters.paypal import PayPalClient
from config import PaypalConfig
from home.models import PaypalTransaction
from services.balance import BalanceRepository


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
        payment_transaction = PaypalTransaction()
        payment_transaction.amount = amount
        payment_transaction.user = user
        payment_transaction.payment_id = payment_id
        payment_transaction.save()

    else:
        payment_link = None

    return JsonResponse({'payment_link': payment_link, 'receiver_info': receiver_info.get(payment_type)})


# Mock exchange rate
EXCHANGE_RATE = 23000  # 1 USD = 23,000 VND


def get_qr_code(request):
    amount = float(request.GET.get('amount'))
    amount_vnd = amount * EXCHANGE_RATE

    # Mock response with bank details and QR code
    bank_info = {
        'qr_code': 'https://example.com/qr-code-image.png',  # Replace with actual QR code generator URL
        'bank_name': 'VN Bank',
        'account_number': '123456789',
        'amount_vnd': amount_vnd
    }

    return JsonResponse(bank_info)


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


def paypal_cancel_callback(request):
    # Mock payment success callback
    data = json.loads(request.body)

    return JsonResponse({'message': 'Payment failed', 'data': data}, status=400)


def paypal_webook(request):
    # Mock payment success callback
    data = json.loads(request.body)
    # get url params
    params = request.GET.__dict__['_iterable']

    print("########### Webhook ###########")
    print(data)
    print(params)


    # return the data
    return JsonResponse({'data': data, 'params': params}, status=200)
