from datetime import timedelta

from django.db import transaction, close_old_connections
from django.db.models import Q
from django.template.loader import render_to_string

from adapters.kafka_adapter import make_kafka_publisher
from adapters.kafka_adapter._base import BaseHandler
from marshmallow import Schema, fields, INCLUDE
from typing import Dict, Any
from tenacity import RetryError

from adapters.mail import EmailSender
from config import KafkaConfig, APPConfig, MailSenderConfig
from home.models import Vps, SystemCounter
from .exception import DBInsertFailed


class MessageType:
    MAIL = 'mail'
    SMS = 'sms'


class TemplateMapping:
    REGISTER = 'mail/register.html'
    VERIFY_EMAIL = 'mail/verify_email.html'
    CREATE_VPS = 'mail/create_vps.html'
    CONFIRM_REGISTRATION = 'mail/confirm_registration.html'


COMMON_DATA = {
    'app_name': APPConfig.APP_NAME,
    'app_domain': APPConfig.APP_DOMAIN,
    'platform_name': f'{APPConfig.APP_NAME} Services'
}


class SendMail(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            type = fields.String(default=MessageType.MAIL)
            data = fields.Dict()
            template = fields.String(required=False)

            class Meta:
                unknown = INCLUDE

        return MySchema()

    def __make_connection(self):
        close_old_connections()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()

        template_name = payload.get('template')
        message_type = payload.get('type')
        data = payload.get('data', {})
        receiver = payload.get('receiver')
        subject = data.get('subject')
        data['common_information'] = COMMON_DATA

        if not template_name:
            try:
                template_name = getattr(TemplateMapping, message_type.upper())
            except:
                template_name = TemplateMapping.REGISTER

        # if template_name != 'mail/register.html':
        #     return

        # Render the template with the provided data
        html_content = render_to_string(template_name, data)
        sender = EmailSender(MailSenderConfig.MAIL_SERVER, MailSenderConfig.MAIL_PORT,
                             MailSenderConfig.MAIL_USERNAME, MailSenderConfig.MAIL_PASSWORD)

        sender.send(MailSenderConfig.MAIL_USERNAME, receiver, subject, html_content, is_html=True)
        return True


class InVPSCreated(BaseHandler):
    def __init__(self) -> None:
        super().__init__()

    def _get_schema(self) -> Schema:
        class MySchema(Schema):
            vps_id = fields.String(required=True)

        return MySchema()

    def _handle(self, payload: Dict[str, Any]) -> None:
        close_old_connections()

        vps_id = payload.get('vps_id')
        vps = Vps.objects.filter(id=vps_id).first()
        if not vps:
            return False

        user = vps.user
        user.vps_len = Vps.objects.filter(user=user).count()  # Count user's VPS instances
        user.save()

        counter = SystemCounter.objects.filter(user=user, type=SystemCounter.CounterType.VPS).first()
        if not counter:
            counter = SystemCounter()
            counter.user = user
            counter.type = SystemCounter.CounterType.VPS
            counter.save()

        count_plan = Vps.objects.filter(user=user, plan_id=vps.plan_id).filter(~Q(_deleted=True)).count()
        counter.data[SystemCounter.KEYGEN.vps(plan_id=vps.plan_id)] = count_plan
        counter.save()

        return True
