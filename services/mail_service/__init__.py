from adapters.kafka_adapter import make_kafka_publisher
from config import NotificationGatewayConfig
from services.invoice import get_now


class VPSMailService:
    def __init__(self):
        self.publisher = make_kafka_publisher(NotificationGatewayConfig)

    def send_register_email(self, user):
        now = get_now()
        self.publisher.publish('send_mail', {
            'type': 'REGISTER',
            'receiver': user.email,
            'data': {
                "subject": "Welcome to World Sever",
                'recipient_name': user.username,
                'platform_name': 'World Sever',
                'current_year': now.year
            }
        })

    def send_verify_email(self, user, token):
        now = get_now()
        self.publisher.publish('send_mail', {
            'type': 'VERIFY_EMAIL',
            'receiver': user.email,
            'data': {
                "subject": "World Sever - Verify Your Email Address",
                'recipient_name': user.username,
                'platform_name': 'World Sever',
                'verification_link': f'https://worldsever.com/verify?token={token}',
                'current_year': now.year
            }
        })

    def send_vps_created_email(self, user, vps):
        now = get_now()
        self.publisher.publish('send_mail', {
            'type': 'CREATE_VPS',
            'receiver': user.email,
            'data': {
                "subject": "Your VPS has been created successfully",
                'customer_name': user.username,
                'vps_hostname': vps.hostname,
                'vps_ip': vps.ip,
                'vps_os': vps.os,
                'vps_username': vps.username,
                'vps_password': vps.password,
                'current_year': now.year,
                'platform_name': 'WorldSever VPS Services'
            }
        })
