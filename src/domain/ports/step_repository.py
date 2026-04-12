from typing import Protocol, List
import uuid
from src.domain.models.step import Step
from src.domain.models.user import UserID


class IStepRepository(Protocol):
    """Протокол репозитория шагов плана обучения"""

    async def create_many(self, steps: List[Step]) -> List[Step]:
        """Создать шаги плана обучения"""
        ...

    async def get_all_by_user_id(self, user_id: UserID) -> List[Step]:
        """Получить все шаги пользователя"""
        ...
