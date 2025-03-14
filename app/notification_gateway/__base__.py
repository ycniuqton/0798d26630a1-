from config import NotificationGatewayConfig
from .__handlers__ import SendMail, InVPSCreated
from adapters.kafka_adapter import HandlerFactory
from adapters.kafka_adapter.consumer import KafkaListener

handlers = {
    'send_mail': SendMail(),
    'vps_created': InVPSCreated(),
}


def run():
    handler_factory = HandlerFactory(handlers=handlers)
    listener = KafkaListener(
        NotificationGatewayConfig,
        handler_factory=handler_factory,
    )
    listener.listen()
