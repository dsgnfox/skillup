from typing import Protocol, List, Optional
import uuid
from src.domain.models.plan import Plan
from src.domain.models.user import UserID


class IPlanRepository(Protocol):
    """Протокол репозитория планов обучения"""

    async def create(self, plan: Plan) -> Plan:
        """Создание плана обучения"""
        ...

    async def get_by_id(self, plan_id: uuid.UUID) -> Optional[Plan]:
        """Получить план по ID"""
        ...

    async def get_by_user_id(self, user_id: UserID) -> List[Plan]:
        """Получить планы пользователя"""
        ...

    async def get_all_by_user_id(self, user_id: UserID) -> List[Plan]:
        """Получить все планы пользователя"""
        ...

    async def delete(self, plan_id: uuid.UUID) -> None:
        """Удаление плана"""
        ...

    async def save(self, plan: Plan) -> Plan:
        """Универсальный save (create/update)"""
        ...
