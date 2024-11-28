from datetime import datetime, timedelta

from django.db.models import Q
from django.utils import timezone

from adapters.kafka_adapter import make_kafka_publisher
from config import KafkaConfig
from services.app_setting import AppSettingRepository
from services.invoice import get_now
from services.report import TopUpCounter, RefundCounter, InvoicePaidCounter, OrderCounter
from .__base__ import BaseJob
from adapters.redis_service import CachedVpsStatRepository
from home.models import Vps, VpsStatus, Invoice, TriggeredOnceEvent, Ticket


class UpdateVpsStat(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        print("Updating VPS stats")
        cvr = CachedVpsStatRepository()
        all_vps = Vps.objects.filter(~Q(_deleted=True)).all()
        vps_ids = [vps.linked_id for vps in all_vps if vps.linked_id]
        cvr.reload(vps_ids)
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
            if invoice.is_suspend_triggered():
                continue
            publisher.publish('check_suspend_vps', {
                'invoice_id': invoice.id,
            })


class ArchiveVPS(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        print("Archiving VPS")
        pivot = get_now() - timedelta(hours=AppSettingRepository().VPS_AUTO_ARCHIVE)
        list_vps = Vps.objects.filter(status=VpsStatus.ERROR, _created__lt=pivot).all()

        for vps in list_vps:
            vps._deleted = True
            vps.save()


class CollectReport(BaseJob):
    """
    Example of a job that inherits from BaseJob.
    This job prints a message when run.
    """

    def run(self):
        print("Collecting report")

        TopUpCounter().update(get_now())
        InvoicePaidCounter().update(get_now())
        OrderCounter().update(get_now())
        RefundCounter().update(get_now())


class CheckTicketExpired(BaseJob):
    def run(self):
        now = get_now()
        open_ticket = Ticket.objects.filter(status=Ticket.TicketStatus.OPEN).all()
        for ticket in open_ticket:
            last_msg = ticket.messages.last()

            last_action = now
            if last_msg:
                last_action = last_msg._created
            else:
                last_action = ticket._created

            if last_action + timedelta(days=3) < now:
                ticket.status = Ticket.TicketStatus.EXPIRED
                ticket.save()
