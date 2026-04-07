from src.domain.exceptions.default_exception import DefaultException


class InfraException(DefaultException):
    """Исключение слоя инфраструктуры"""

    def __init__(self, message: str | None = None):
        super().__init__(message)
