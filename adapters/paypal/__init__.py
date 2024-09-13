import paypalrestsdk


class PayPalClient:
    def __init__(self, mode, client_id, client_secret):
        """
        Initializes the PayPal client with necessary configuration.

        :param mode: Mode of PayPal API ("sandbox" or "live")
        :param client_id: PayPal client ID
        :param client_secret: PayPal client secret
        """
        self.mode = mode
        self.client_id = client_id
        self.client_secret = client_secret
        # Configure the PayPal SDK
        paypalrestsdk.configure({
            "mode": self.mode,  # Use "sandbox" for testing or "live" for production
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })

    def generate_payment_link(self, total, currency, description, return_url, cancel_url):
        """
        Generates a PayPal payment link for the client.

        :param total: Total amount of the transaction (e.g., "25.00")
        :param currency: Currency of the payment (e.g., "USD")
        :param description: Description of the transaction
        :param return_url: URL to which PayPal redirects after payment approval
        :param cancel_url: URL to which PayPal redirects after payment cancellation
        :return: The approval URL (payment link) or None if failed
        """
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": return_url,  # Redirect URL after successful payment
                "cancel_url": cancel_url  # Redirect URL if the user cancels
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": description,
                        "sku": "001",
                        "price": total,
                        "currency": currency,
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": total,
                    "currency": currency
                },
                "description": description
            }]
        })

        # Try to create the payment and return the approval URL
        if payment.create():
            for link in payment.links:
                if link.rel == "approval_url":
                    return link.href
        else:
            print(f"Payment creation failed: {payment.error}")
            return None

    def verify_payment(self, payment_id, payer_id):
        """
        Verifies a payment by executing it with the given paymentId and payerId.

        :param payment_id: The payment ID received in the return URL
        :param payer_id: The Payer ID received in the return URL
        :return: The payment object if verified successfully, otherwise None
        """
        try:
            # Retrieve the payment object by its ID
            payment = paypalrestsdk.Payment.find(payment_id)

            # If payment exists, try to execute it
            if payment and payment.execute({"payer_id": payer_id}):
                if payment.state == "approved":
                    print("Payment approved successfully")
                    return payment
                else:
                    print("Payment not approved")
                    return None
            else:
                print(f"Failed to execute payment: {payment.error}")
                return None
        except paypalrestsdk.ResourceNotFound as error:
            print(f"Payment not found: {error}")
            return None


if __name__ == "__main__":
    config = {
        "mode": "sandbox",  # Use "live" for production mode
        "client_id": "AeELEZ3HjcqAqDmWckZZIIiAHFEOY6XIOvRzaTbgOGmp2MAgTdrD_0DVyHH89vmfUZQmbacMWvIDO41o",
        "client_secret": "EPdkV4a6b_FB4LvmXwR_JXx0jikf9Bj5TkJOG01j3dLK1ULGst0CUvODsOG9B2-lRt0STXBM7xXffh3L"
    }

    client = PayPalClient(
        mode=config.get("mode"),
        client_id=config.get("client_id"),
        client_secret=config.get("client_secret")
    )
    # paymentId=PAYID-M3R7U4Y9U845543KB0673314&token=EC-2KD888403D855480W&PayerID=QWAKLCAC34ZMN
    data = client.verify_payment(
        payment_id="PAYID-M3R7U4Y9U845543KB0673314",
        payer_id="QWAKLCAC34ZMN"
    )

    print(data)
