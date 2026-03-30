from src.domain.exceptions.default_exception import DefaultException


class TelegramAlreadyAdded(DefaultException):
    """Телеграм уже привязан к пользователю"""

    def __init__(self):
        super().__init__(message=None)
