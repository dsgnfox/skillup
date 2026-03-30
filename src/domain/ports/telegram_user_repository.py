from typing import Optional, Protocol
from src.domain.models.telegram_user import TelegramUser
from src.domain.models.user import User, UserID


class ITelegramUserRepository(Protocol):
    """Протокол репозитория пользователей телеграм"""

    async def get_by_user_id(self, user_id: UserID) -> Optional[TelegramUser]:
        """Получить Telegram данные по user_id"""
        ...

    async def save(self, telegram_user: TelegramUser) -> None:
        """Сохранить Telegram пользователя"""
        ...

    async def exists(self, telegram_id: int) -> bool:
        """Проверить, есть ли Telegram пользователь"""
        ...
