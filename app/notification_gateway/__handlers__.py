from datetime import timedelta

from django.db import transaction, close_old_connections
from django.template.loader import render_to_string

from adapters.kafka_adapter import make_kafka_publisher
from adapters.kafka_adapter._base import BaseHandler
from marshmallow import Schema, fields, INCLUDE
from typing import Dict, Any
from tenacity import RetryError

from adapters.mail import EmailSender
from config import KafkaConfig, APPConfig, MailSenderConfig
from .exception import DBInsertFailed


class MessageType:
    MAIL = 'mail'
    SMS = 'sms'


class TemplateMapping:
    REGISTER = 'mail/register.html'
    VERIFY_EMAIL = 'mail/verify_email.html'
    CREATE_VPS = 'mail/create_vps.html'


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
