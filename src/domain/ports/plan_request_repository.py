from typing import Protocol

from src.domain.models.plan_request import PlanRequest
from src.domain.models.user import UserID
from src.domain.ports.dto.plan_request_update_dto import PlanRequestUpdateDTO


class IPlanRequestRepository(Protocol):
    """Протокол репозитория запросов на создание планов обучения"""

    async def create(self, plan_request: PlanRequest) -> PlanRequest:
        """создать запрос на план обучения"""
        ...

    async def update(self, plan_request: PlanRequestUpdateDTO) -> PlanRequest:
        """обновить запрос на план обучения"""
        ...

    async def get_all_by_user_id(self, user_id: UserID) -> list[PlanRequest]:
        """Получить запросы на планы обучения по ID пользователя"""
        ...
