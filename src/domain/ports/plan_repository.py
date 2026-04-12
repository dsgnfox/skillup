from typing import Protocol, List, Optional
import uuid
from src.domain.models.plan import Plan
from src.domain.models.user import UserID


class IPlanRepository(Protocol):
    """Протокол репозитория планов обучения"""

    async def create(self, plan: Plan) -> Plan:
        """создать план обучения"""
        ...

    async def get_all_by_user_id(self, user_id: UserID) -> List[Plan]:
        """Получить все планы пользователя"""
        ...
