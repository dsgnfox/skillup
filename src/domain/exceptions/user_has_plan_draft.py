from src.domain.exceptions.default_exception import DefaultException


class UserHasDraftPlan(DefaultException):
    """У пользователя есть план обучения ожидающий старта"""

    def __init__(self):
        super().__init__(message=None)
