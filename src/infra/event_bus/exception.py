from src.infra.exceptions.infra_exception import InfraException


class EventBusException(InfraException):
    """Исключение шины событий"""

    def __init__(self, message: str | None = None):
        super().__init__(message)


class RedisEventBusException(InfraException):
    """Исключение Redis шины событий"""

    def __init__(self, message: str | None = None):
        super().__init__(f"{self.__class__.__name__} :: {message}")
