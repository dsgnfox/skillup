from typing import Protocol, TypedDict
from attr import dataclass
from src.application.commands.base_command import BaseCommand
from src.domain.models.plan_request import PlanRequest


class StepItem(TypedDict):
    title: str
    description: str


class PlanCreationCompletePayload(TypedDict):
    steps: list[StepItem]
    is_success: bool
    error: str | None


class IPlanCreationCompleteCommand(Protocol):
    async def execute(self, payload: PlanCreationCompletePayload) -> PlanRequest: ...


class PlanCreationCompleteCommand(BaseCommand):
    """Команда завершения создания плана обучения"""

    pass
