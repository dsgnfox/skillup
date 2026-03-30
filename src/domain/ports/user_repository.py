from typing import Optional, Protocol
from src.domain.models.user import User, UserID


class IUserRepository(Protocol):
    """Протокол репозитория пользователей"""

    async def save(self, user: User) -> None:
        """Сохранить пользователя"""
        ...
