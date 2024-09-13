import paypalrestsdk
import logging

# Configure your PayPal SDK
paypalrestsdk.configure({
    "mode": "sandbox",  # Use "live" for production mode
    "client_id": "AeELEZ3HjcqAqDmWckZZIIiAHFEOY6XIOvRzaTbgOGmp2MAgTdrD_0DVyHH89vmfUZQmbacMWvIDO41o",
    "client_secret": "EPdkV4a6b_FB4LvmXwR_JXx0jikf9Bj5TkJOG01j3dLK1ULGst0CUvODsOG9B2-lRt0STXBM7xXffh3L"
})


def create_payment():
    # Create the payment object
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://157.66.24.255/payment/execute",  # Your success URL
            "cancel_url": "http://157.66.24.255/payment/cancel"},  # Your cancel URL
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": "Test Item",
                    "sku": "001",
                    "price": "25.00",
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": "25.00",
                "currency": "USD"},
            "description": "This is a test payment."}]})

    # Create payment and check if successful
    if payment.create():
        print("Payment created successfully")
        for link in payment.links:
            if link.rel == "approval_url":
                # This is the redirect URL that the client will click to pay
                approval_url = link.href
                print("Redirect for approval: {}".format(approval_url))
                return approval_url
    else:
        print(payment.error)
        return None


payment_url = create_payment()
print(f"Send this URL to the client to complete the payment: {payment_url}")
