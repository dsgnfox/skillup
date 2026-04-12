from typing import Protocol
import uuid
from attr import dataclass
from src.application.commands.base_command import BaseCommand
from src.domain.models.plan_request import PlanRequestStatus
from src.domain.models.plan import Plan, PlanStatus
from src.domain.models.step import Step, StepStatus
from src.domain.ports.plan_repository import IPlanRepository
from src.domain.ports.plan_request_repository import IPlanRequestRepository
from src.domain.ports.step_repository import IStepRepository
from src.domain.ports.user_repository import IUserRepository
from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.domain.ports.dto.plan_request_update_dto import PlanRequestUpdateDTO
from src.infra.exceptions.active_plan_exists_error import ActivePlanExistsError


@dataclass(frozen=True)
class StepItem:
    title: str
    description: str


@dataclass(frozen=True)
class PlanCreationCompletePayload:
    plan_request_id: uuid.UUID
    steps: list[StepItem]
    is_success: bool
    error: str | None


class IPlanCreationCompleteCommand(Protocol):
    async def execute(self, payload: PlanCreationCompletePayload) -> Plan | None: ...


class PlanCreationCompleteCommand(BaseCommand):
    """Команда завершения создания плана обучения"""

    def __init__(
        self,
        plan_repo: IPlanRepository,
        plan_request_repo: IPlanRequestRepository,
        step_repo: IStepRepository,
        user_repo: IUserRepository,
        telegram_user_repo: ITelegramUserRepository,
    ):
        self.plan_repo = plan_repo
        self.plan_request_repo = plan_request_repo
        self.step_repo = step_repo
        self.user_repo = user_repo
        self.telegram_user_repo = telegram_user_repo

    async def execute(self, payload: PlanCreationCompletePayload) -> Plan | None:
        # Получаем информацию о запросе на создание плана
        plan_request = await self.plan_request_repo.get_by_id(payload.plan_request_id)

        if not plan_request:
            return

        # Проверяем, что нет уже активного плана обучения для пользователя
        active_plans = await self.plan_repo.get_all_by_user_id(plan_request.user_id)
        if any(plan.status == PlanStatus.IN_PROGRESS for plan in active_plans):
            raise ActivePlanExistsError(str(plan_request.user_id))

        # Если есть ошибка в генерации плана, обновляем запрос и возвращаем None
        if not payload.is_success:
            updated_plan_request = PlanRequestUpdateDTO(
                id=plan_request.id,
                status=PlanRequestStatus.FAILED,
                error_msg=payload.error,
            )
            await self.plan_request_repo.update(updated_plan_request)
            return None

        # Создаем шаги обучения с привязкой к плану
        plan_id = uuid.uuid7()
        steps = [
            Step(
                id=uuid.uuid7(),
                name=step_item.title,
                content=step_item.description,
                status=StepStatus.DRAFT,
                user_id=plan_request.user_id,
                plan_id=plan_id,
            )
            for step_item in payload.steps
        ]

        # Создаем план обучения
        plan = Plan(
            id=plan_id,
            name=f"План обучения {plan_request.created_at.strftime('%d.%m.%Y')}",
            user_id=plan_request.user_id,
            status=PlanStatus.IN_PROGRESS,
        )

        # Сохраняем шаги и план
        await self.plan_repo.create(plan)
        await self.step_repo.create_many(steps)

        # Обновляем запрос на создание плана
        updated_plan_request = PlanRequestUpdateDTO(
            id=plan_request.id,
            status=PlanRequestStatus.COMPLETED,
            plan_id=plan_id,
        )
        await self.plan_request_repo.update(updated_plan_request)

        return plan
