from typing import Any

from src.domain.events.user_register import UserRegisterEvent


class UserRegistrationEventHandler:
    """Обработчик события регистрации пользователя"""

    def __init__(self) -> None:
        pass

    def __call__(self, event: UserRegisterEvent) -> Any:
        pass
