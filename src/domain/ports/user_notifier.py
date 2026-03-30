from typing import Protocol

from src.domain.models.user import UserID


class IUserNotifier(Protocol):
    """Протокол сервиса уведомления пользователя"""

    async def notify(self, user_id: UserID, message: str):
        """Отправить уведомление пользователю"""
        ...
