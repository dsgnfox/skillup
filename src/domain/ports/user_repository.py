from typing import Optional, Protocol
from src.domain.models.user import User, UserID


class IUserRepository(Protocol):
    async def get_by_id(self, user_id: UserID) -> Optional[User]:
        """Получить пользователя по ID"""
        ...
    
    async def save(self, user: User) -> None:
        """Сохранить/обновить пользователя"""
        ...
    
    async def exists(self, user_id: UserID) -> bool:
        """Проверить существование пользователя"""
        ...