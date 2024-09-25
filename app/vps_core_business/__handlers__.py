from datetime import timedelta

from django.db import transaction, close_old_connections

from adapters.kafka_adapter import make_kafka_publisher
from adapters.kafka_adapter._base import BaseHandler
from marshmallow import Schema, fields, INCLUDE
from typing import Dict, Any
from tenacity import RetryError

from config import KafkaConfig
from home.models import Vps, VpsStatus, User, TriggeredOnceEvent, Invoice
from adapters.kafka_adapter._exceptions import SkippableException
from services.app_setting import AppSettingRepository
from services.invoice import InvoiceRepository, get_billing_cycle, get_now
from services.virtualizor_manager import VirtualizorManager
from services.vps_log import VPSLogger
from core import settings

if settings.APPConfig.APP_ROLE == 'admin':
    from services.vps import VPSService
else:
    from services.vps import CtvVPSService as VPSService

from .exception import DBInsertFailed


class CreateVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            hostname = fields.String(required=True)
            password = fields.String(required=True)
            serid = fields.String(required=False)
            plid = fields.String(required=True)
            osid = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)
        error = ""
        try:
            response = service.create(payload)
            return True
        except RetryError as e:
            error = e.last_attempt.exception()
        except Exception as e:
            error = e

        VPSService.error(vps.id, error)


class StartVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.start(vps.linked_id)
        except:
            raise SkippableException("Failed to start VPS")


class StopVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.stop(vps.linked_id)
        except:
            raise SkippableException("Failed to stop VPS")


class DeleteVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.delete(vps.linked_id)
        except:
            raise SkippableException("Failed to delete VPS")


class RestartVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.restart(vps.linked_id)
        except:
            raise SkippableException("Failed to restart VPS")


class SuspendVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.suspend(vps.linked_id)
        except:
            raise SkippableException("Failed to suspend VPS")


class DeleteVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.delete(vps.linked_id)
            if not vps.linked_id:
                vps._deleted = True
                vps.status = VpsStatus.DELETED
                vps.save()
        except:
            raise SkippableException("Failed to delete VPS")


class UnSuspendVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.unsuspend(vps.linked_id)
        except:
            raise SkippableException("Failed to unsuspend VPS")


class GiveVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")
        sender_email = vps.user.email
        receiver = User.objects.filter(id=payload.get('receiver_id')).first()

        if not receiver:
            return False

        vps.user = receiver
        vps.save()

        VPSLogger().log(receiver, vps, 'receive', 'received', f'Received VPS from {sender_email}')


class RebuildVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")
        payload['vps_id'] = vps.linked_id
        image_version = payload.get('raw_data').get('image_version')
        username = payload.get('username')
        base_url = settings.ADMIN_CONFIG.URL
        api_key = settings.ADMIN_CONFIG.API_KEY

        service = VPSService(base_url, api_key)

        try:
            response = service.rebuild(payload)
        except:
            service.error(vps.id, "Failed to rebuild VPS")
            raise SkippableException("Failed to rebuild VPS")


class ExpiredVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        if not vps.is_expired():
            return False

        if vps.auto_renew:
            # send suspend
            publisher = make_kafka_publisher(KafkaConfig)

            publisher.publish('gen_invoice', {
                'user_id': vps.user_id,
                'items': [vps.id]
            })

        VPSLogger().log(vps.user, vps, 'expire', 'expired', f'VPS has expired')

        trigger_event = TriggeredOnceEvent()
        trigger_event.vps_id = vps.id
        trigger_event.key = vps.cycle
        trigger_event.event_name = TriggeredOnceEvent.EventName.VPS_EXPIRED
        trigger_event.user = vps.user
        trigger_event.save()


class InvoiceExpired(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            invoice_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        invoice = Invoice.objects.filter(id=payload['invoice_id']).first()
        if not invoice:
            raise DBInsertFailed("Missing Order")

        if not invoice.is_expired():
            return False

        invoice.status = Invoice.Status.EXPIRED
        invoice.save()

        # send suspend
        publisher = make_kafka_publisher(KafkaConfig)

        for line in invoice.lines.all():
            publisher.publish('delete_vps', {
                'vps_id': line.vps_id
            })

        trigger_event = TriggeredOnceEvent()
        trigger_event.invoice_id = invoice.id
        trigger_event.event_name = TriggeredOnceEvent.EventName.INVOICE_EXPIRED
        trigger_event.user = invoice.user
        trigger_event.save()


class GenerateInvoice(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            user_id = fields.String(required=True)
            items = fields.List(fields.String, required=True)
            cycle = fields.String(required=False)
            from_time = fields.DateTime(required=False)
            to_time = fields.DateTime(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        user = User.objects.filter(id=payload['user_id']).first()
        cycle = payload.get('cycle')
        from_time = payload.get('from_time')
        to_time = payload.get('to_time')

        if not cycle:
            cycle, from_time, to_time = get_billing_cycle(get_now())

        if not user:
            raise DBInsertFailed("Missing User")

        list_vps = Vps.objects.filter(id__in=payload['items']).all()

        invoice_repo = InvoiceRepository()
        invoice = invoice_repo.create(user.id, items=list_vps, cycle=cycle, from_time=from_time,
                                      to_time=to_time)

        for vps in list_vps:
            vps.cycle = cycle
            vps.end_time = to_time
            vps.save()

        publisher = make_kafka_publisher(KafkaConfig)
        publisher.publish('charge_invoice', payload={
            'invoice_id': invoice.id
        })


class BalanceToppedUp(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            user_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        user = User.objects.filter(id=payload['user_id']).first()

        open_invoices = Invoice.objects.filter(user=user, status='open').all()

        publisher = make_kafka_publisher(KafkaConfig)
        for invoice in open_invoices:
            publisher.publish('charge_invoice', payload={
                'invoice_id': invoice.id
            })


class ChargeInvoice(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            invoice_id = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        invoice = Invoice.objects.filter(id=payload['invoice_id']).first()

        if not invoice:
            return

        publisher = make_kafka_publisher(KafkaConfig)
        invoice_repo = InvoiceRepository()
        app_setting = AppSettingRepository()

        if not invoice_repo.charge(invoice):
            if invoice._created + timedelta(days=app_setting.SUFFICIENT_BALANCE_SUSPEND_DAYS) > get_now():
                return
            invoice_lines = invoice.lines.all()
            for line in invoice_lines:
                payload = {
                    "vps_id": line.vps_id
                }
                publisher.publish('suspend_vps', payload)


class RestoreVPS(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)
            abs_path = fields.String(required=True)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()
        vps = Vps.objects.filter(id=payload['vps_id']).first()
        if not vps:
            raise DBInsertFailed("Missing Order")
        abs_path = payload.get('abs_path')

        virtualizor_manager = VirtualizorManager()
        try:
            virtualizor_manager.restore_vps(vps.linked_id, abs_path)
        except:
            raise SkippableException("Failed to restart VPS")
