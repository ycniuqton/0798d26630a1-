from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from home.models import RefundRequest, VpsStatus
from services.vps_log import VPSLogger


class RefundService:
    @staticmethod
    def create(invoice_line):
        vps = invoice_line.vps
        if not vps.is_refundable:
            return False

        existed_refund_request = RefundRequest.objects.filter(vps=vps, status__in=[
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
        vps = refund_request.vps
        user = refund_request.user

        publisher = make_kafka_publisher(KafkaConfig)
        payload = {
            "user_id": refund_request.vps.user_id,
            "items": [refund_request.vps_id],
        }
        publisher.publish('gen_refund_invoice', payload)

        VPSLogger().log(user, vps, 'delete', VpsStatus.DELETING)
        payload = {
            "vps_id": vps.id
        }
        publisher.publish('delete_vps', payload)

    @staticmethod
    def reject(refund_request):
        refund_request.status = RefundRequest.RefundRequestStatus.REJECTED
        refund_request.save()

        refund_request.vps.status = VpsStatus.ACTIVE
        refund_request.vps.save()
