from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from home.models import RefundRequest, VpsStatus


class RefundService:
    @staticmethod
    def create(invoice_line):
        vps = invoice_line.vps
        if not vps.is_refundable:
            return False

        existed_refund_request = RefundRequest.objects.filter(vps=vps, status_in=[
            RefundRequest.RefundRequestStatus.PENDING, RefundRequest.RefundRequestStatus.APPROVED]).all()
        if existed_refund_request:
            return False

        RefundRequest.objects.create(
            user=vps.user,
            vps=vps,
            amount=invoice_line.amount,
        )

    @staticmethod
    def approve(refund_request):
        refund_request.status = RefundRequest.RefundRequestStatus.APPROVED
        refund_request.save()
        refund_request.vps._deleted = True
        refund_request.vps.save()

        publisher = make_kafka_publisher(KafkaConfig)
        payload = {
            "vps_id": refund_request.vps.id,
            "items": [refund_request.user.id],
        }
        publisher.publish('gen_refund_invoice', payload)

    @staticmethod
    def reject(refund_request):
        refund_request.status = RefundRequest.RefundRequestStatus.REJECTED
        refund_request.save()

        refund_request.vps.status = VpsStatus.ACTIVE
        refund_request.vps.save()
