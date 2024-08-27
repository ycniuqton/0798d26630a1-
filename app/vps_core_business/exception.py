from services.kafka_adapter._exceptions import InvalidEventPayload, SkippableException


class DBInsertFailed(SkippableException):
    pass
