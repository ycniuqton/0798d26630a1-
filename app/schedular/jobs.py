from datetime import datetime, timedelta

from django.utils import timezone

from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.app_setting import AppSettingRepository
from services.invoice import get_now
from .__base__ import BaseJob
from adapters.redis_service import CachedVpsStatRepository
from home.models import Vps, VpsStatus, Invoice, TriggeredOnceEvent


class UpdateVpsStat(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        cvr = CachedVpsStatRepository()
        cvr.reload()
        print("Vps stats updated!")


class CheckVPSExpired(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        # filter not suspended vps
        list_vps = Vps.objects.filter(end_time__lt=get_now()).all()

        for vps in list_vps:
            is_expire_triggered = vps.is_expire_triggered()
            if is_expire_triggered is None or is_expire_triggered:
                continue

            publisher = make_kafka_publisher(KafkaConfig)
            publisher.publish('vps_expired', {
                'vps_id': vps.id,
            })


class CheckInvoiceExpired(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        # filter not suspended vps
        list_invoice = Invoice.objects.filter(due_date__lt=get_now(), status='open').all()

        for invoice in list_invoice:
            is_expire_triggered = invoice.is_expire_triggered()
            if is_expire_triggered is None or is_expire_triggered:
                continue

            publisher = make_kafka_publisher(KafkaConfig)
            publisher.publish('invoice_expired', {
                'invoice_id': invoice.id,
            })


class CheckSuspendVPS(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        list_invoice = Invoice.objects.filter(status='open').all()
        app_setting = AppSettingRepository()
        publisher = make_kafka_publisher(KafkaConfig)

        for invoice in list_invoice:
            if invoice.is_suspend_triggered():
                continue
            if invoice._created + timedelta(days=app_setting.SUFFICIENT_BALANCE_SUSPEND_DAYS) > get_now():
                continue

            for line in invoice.lines.all():
                publisher.publish('suspend_vps', {
                    'vps_id': line.vps_id,
                })

            trigger_event = TriggeredOnceEvent()
            trigger_event.invoice_id = invoice.id
            trigger_event.event_name = TriggeredOnceEvent.EventName.INVOICE_SUSPENDED
            trigger_event.user = invoice.user
            trigger_event.save()
