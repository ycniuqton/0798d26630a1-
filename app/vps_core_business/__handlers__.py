from django.db import transaction, close_old_connections
from adapters.kafka_adapter._base import BaseHandler
from marshmallow import Schema, fields, INCLUDE
from typing import Dict, Any
from tenacity import RetryError

from home.models import Vps, VpsStatus, User
from adapters.kafka_adapter._exceptions import SkippableException
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
            serid = fields.String(required=True)
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
            vps.ip = response.get('ip')
            vps.linked_id = response.get('id')
            vps.status = VpsStatus.ON
            vps.save()
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
            vps.status = VpsStatus.ON
            vps.save()
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
            vps.status = VpsStatus.OFF
            vps.save()
        except:
            raise SkippableException("Failed to stop VPS")


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
            vps.status = VpsStatus.ON
            vps.save()
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
            vps.status = VpsStatus.SUSPENDED
            vps.save()
        except:
            raise SkippableException("Failed to suspend VPS")


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
            vps.status = VpsStatus.ON
            vps.save()
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


