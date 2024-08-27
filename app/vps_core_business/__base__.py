from config import KafkaConfig
from .__handlers__ import CreateVPS
from services.kafka_adapter._handler_factory import HandlerFactory
from services.kafka_adapter.consumer import KafkaListener

handlers = {
    'create_vps': CreateVPS()
}


def run():
    handler_factory = HandlerFactory(handlers=handlers)
    listener = KafkaListener(
        KafkaConfig,
        handler_factory=handler_factory,
    )
    listener.listen()
