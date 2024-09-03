from config import KafkaConfig
from .__handlers__ import CreateVPS, StartVPS, StopVPS, SuspendVPS, UnSuspendVPS, RestartVPS
from adapters.kafka_adapter import HandlerFactory
from adapters.kafka_adapter.consumer import KafkaListener

handlers = {
    'create_vps': CreateVPS(),
    'start_vps': StartVPS(),
    'stop_vps': StopVPS(),
    'restart_vps': RestartVPS(),
    'suspend_vps': SuspendVPS(),
    'unsuspend_vps': UnSuspendVPS(),
}


def run():
    handler_factory = HandlerFactory(handlers=handlers)
    listener = KafkaListener(
        KafkaConfig,
        handler_factory=handler_factory,
    )
    listener.listen()
