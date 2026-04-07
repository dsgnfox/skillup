from src.domain.exceptions.default_exception import DefaultException


class UserHasActivePlanRequest(DefaultException):
    """Пользователь уже имеет активный запрос на создание плана обучения"""

    def __init__(self):
        super().__init__(message=None)
