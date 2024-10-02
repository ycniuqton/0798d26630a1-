from datetime import datetime, timedelta

from django.db.models import Q
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
        print("Updating VPS stats")
        cvr = CachedVpsStatRepository()
        cvr.reload()
        print("Vps stats updated!")


class CheckVPSExpired(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        print("Checking VPS expired")
        # filter not suspended vps
        list_vps = Vps.objects.filter(end_time__lt=get_now()).filter(~Q(_deleted=True)).all()

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
        print("Checking Invoice expired")
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
        print("Checking Suspend VPS")
        list_invoice = Invoice.objects.filter(status='open').all()
        app_setting = AppSettingRepository()
        publisher = make_kafka_publisher(KafkaConfig)

        for invoice in list_invoice:
            publisher.publish('check_suspend_vps', {
                'invoice_id': invoice.id,
            })

