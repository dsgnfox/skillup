from src.domain.exceptions.default_exception import DefaultException


class UserHasInProcessPlan(DefaultException):
    """Пользователь уже имеет активный план обучения"""

    def __init__(self):
        super().__init__(message=None)
