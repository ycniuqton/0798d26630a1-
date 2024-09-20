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


class VPSCreated(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')

        if not identifier:
            return False

        vps = Vps.objects.filter(identifier=identifier).first()
        if not vps:
            return False

        ips = data.get('ips', {})
        vps.ip = next(iter(ips.values()), None)
        vps.linked_id = data.get('vpsid')
        vps.status = VpsStatus.ON
        vps.save()


class VPSCreatedError(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')

        if not identifier:
            return False

        vps = Vps.objects.filter(identifier=identifier).first()
        if not vps:
            return False

        vps.status = VpsStatus.ERROR
        vps.meta_data = data
        vps.error_message = "Failed to create VPS"
        vps.save()


class VPSStarted(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ON
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSStartedError(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.OFF
            vps.meta_data = data
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSStopped(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.OFF
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSDeleted(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps._deleted = True
            vps.status = VpsStatus.DELETED
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSStoppedError(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ON
            vps.meta_data = data
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSRestarted(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ON
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSRestartedError(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ERROR
            vps.error_message = "Failed to restart VPS"
            vps.meta_data = data
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSSuspended(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.SUSPENDED
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSSuspendedError(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ERROR
            vps.error_message = "Failed to suspend VPS"
            vps.meta_data = data
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSUnSuspended(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ON
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSRebuilt(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ON
            # vps.os_version = image_version
            # vps.username = username
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")


class VPSRebuiltError(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            identifier = fields.String(required=False)
            data = fields.Dict(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        identifier = payload.get('identifier')
        data = payload.get('data')
        vps = Vps.objects.filter(linked_id=identifier).first()
        if not vps:
            raise DBInsertFailed("Missing Order")

        try:
            vps.status = VpsStatus.ERROR
            vps.error_message = "Failed to rebuild VPS"
            vps.meta_data = data
            vps.save()
        except:
            raise SkippableException("Failed to start VPS")
