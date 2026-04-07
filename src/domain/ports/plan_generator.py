from typing import Protocol

from src.domain.models.plan_request import PlanRequest


class IPlanGeneratorService(Protocol):
    """Протокол сервиса для генерации учебного плана"""

    async def generate(self, plan_request: PlanRequest) -> PlanRequest: ...
