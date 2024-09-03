from django.db import transaction, close_old_connections
from adapters.kafka_adapter._base import BaseHandler
from marshmallow import Schema, fields, INCLUDE
from typing import Dict, Any

from services.vps import VPSService
from home.models import Vps, VpsStatus, User
from adapters.kafka_adapter._exceptions import SkippableException
from services.vps_log import VPSLogger
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

        base_url = "http://127.0.0.1:5000"
        api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

        service = VPSService(base_url, api_key)

        try:
            response = service.create(payload)
            vps.ip = response.get('ip')
            vps.linked_id = response.get('id')
            vps.status = VpsStatus.ON
            vps.save()
        except:
            raise SkippableException("Failed to create VPS")


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

        base_url = "http://127.0.0.1:5000"
        api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

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

        base_url = "http://127.0.0.1:5000"
        api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

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

        base_url = "http://127.0.0.1:5000"
        api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

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

        base_url = "http://127.0.0.1:5000"
        api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

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

        base_url = "http://127.0.0.1:5000"
        api_key = "scrypt:32768:8:1$RL6X6J7bJJiROtTL$5bd54c34882906e9cf41e596c0a2b67f2a256b1492e266642f3c40521e4b4521ff56dfcf84e9deb9e34ea63d6e89de3c089d32041b5269d76f4c11078636aebd"

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


