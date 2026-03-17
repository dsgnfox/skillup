from typing import Optional, Protocol
from src.domain.models.telegram_user import TelegramUser
from src.domain.models.user import UserID

class ITelegramUserRepository(Protocol):
    async def get_by_telegram_id(self, telegram_id: int) -> Optional[TelegramUser]:
        """Получить Telegram данные по telegram_id"""
        ...
    
    async def save(self, telegram_data: TelegramUser, user_id: Optional[UserID] = None) -> None:
        """Сохранить Telegram данные, опционально привязать к User"""
        ...
    
    async def exists(self, telegram_id: int) -> bool:
        """Проверить, есть ли Telegram пользователь"""
        ...
    
    async def get_or_create(self, telegram_id: int, **kwargs) -> TelegramUser:
        """Получить или создать Telegram пользователя"""
        ...
        
