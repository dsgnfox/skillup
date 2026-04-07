from dataclasses import dataclass
from datetime import datetime
from typing import Protocol
import uuid

from src.application.commands.base_command import BaseCommand
from src.domain.events.plan_request_submitted import PlanRequestSubmittedEvent
from src.domain.exceptions.user_has_in_process_plan import UserHasInProcessPlan
from src.domain.exceptions.user_has_active_plan_request import (
    UserHasActivePlanRequest,
)
from src.domain.exceptions.user_has_plan_draft import UserHasDraftPlan
from src.domain.models.plan import PlanStatus
from src.domain.models.plan_request import PlanRequest, PlanRequestStatus
from src.domain.models.user import UserID
from src.domain.ports.event_bus import IEventBus
from src.domain.ports.plan_repository import IPlanRepository
from src.domain.ports.plan_request_repository import IPlanRequestRepository


@dataclass
class CreatePlanPayload:
    user_id: UserID
    request: str  # Запрос пользователя на создание плана обучения


class ICreatePlanCommand(Protocol):
    async def execute(self, payload: CreatePlanPayload) -> PlanRequest: ...


class CreatePlanCommand(BaseCommand):
    """Команда создания плана обучения"""

    MAX_ACTIVE_REQUESTS_PER_USER = 1

    def __init__(
        self,
        plan_request_repo: IPlanRequestRepository,
        plan_repo: IPlanRepository,
        event_bus: IEventBus,
    ):
        self.plan_request_repo = plan_request_repo
        self.plan_repo = plan_repo
        self.event_bus = event_bus

    async def execute(self, payload: CreatePlanPayload) -> PlanRequest:
        user_requests = await self.plan_request_repo.get_all_by_user_id(payload.user_id)
        active_requests = [
            r
            for r in user_requests
            if r.status == PlanRequestStatus.PENDING
            or r.status == PlanRequestStatus.PROCESSING
        ]

        if len(active_requests) >= self.MAX_ACTIVE_REQUESTS_PER_USER:
            raise UserHasActivePlanRequest()

        user_plans = await self.plan_repo.get_all_by_user_id(payload.user_id)

        user_plans_draft = [p for p in user_plans if p.status == PlanStatus.DRAFT]

        if user_plans_draft:
            raise UserHasDraftPlan()

        plans_in_progress = [
            p for p in user_plans if p.status == PlanStatus.IN_PROGRESS
        ]

        if plans_in_progress:
            raise UserHasInProcessPlan()

        plan_request = PlanRequest(
            id=uuid.uuid7(),
            user_id=payload.user_id,
            status=PlanRequestStatus.PENDING,
            request=payload.request,
            created_at=datetime.now(),
        )

        await self.plan_request_repo.create(plan_request)

        await self.event_bus.publish(PlanRequestSubmittedEvent(plan_request))

        return plan_request
