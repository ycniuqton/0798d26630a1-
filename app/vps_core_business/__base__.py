from config import KafkaConfig
from .__handlers__ import CreateVPS, StartVPS, StopVPS, SuspendVPS, UnSuspendVPS, RestartVPS, GiveVPS, RebuildVPS, \
    ExpiredVPS, GenerateInvoice, ChargeInvoice, BalanceToppedUp, InvoiceExpired, DeleteVPS
from adapters.kafka_adapter import HandlerFactory
from adapters.kafka_adapter.consumer import KafkaListener

handlers = {
    'create_vps': CreateVPS(),
    'start_vps': StartVPS(),
    'stop_vps': StopVPS(),
    'delete_vps': DeleteVPS(),
    'restart_vps': RestartVPS(),
    'suspend_vps': SuspendVPS(),
    'unsuspend_vps': UnSuspendVPS(),
    'give_vps': GiveVPS(),
    'rebuild_vps': RebuildVPS(),
    'vps_expired': ExpiredVPS(),
    'gen_invoice': GenerateInvoice(),
    'charge_invoice': ChargeInvoice(),
    'invoice_expired': InvoiceExpired(),
    'balance_topped_up': BalanceToppedUp(),
}


def run():
    handler_factory = HandlerFactory(handlers=handlers)
    listener = KafkaListener(
        KafkaConfig,
        handler_factory=handler_factory,
    )
    listener.listen()
