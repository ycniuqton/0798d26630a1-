from adapters.kafka_adapter._exceptions import SkippableException


class DBInsertFailed(SkippableException):
    pass
