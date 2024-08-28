from adapters.kafka_adapter import SkippableException


class DBInsertFailed(SkippableException):
    pass
