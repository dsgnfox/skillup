import asyncio
from src.domain.models.plan_request import PlanRequest, PlanRequestStatus
from src.domain.ports.dto.plan_request_update_dto import PlanRequestUpdateDTO
from src.domain.ports.plan_generator import IPlanGeneratorService
from src.domain.ports.plan_request_repository import IPlanRequestRepository
from src.infra.background_tasks.generate_plan import generate_plan_celery_task


class PlanGeneratorService(IPlanGeneratorService):
    """Сервис для генерации учебного плана"""

    def __init__(self, plan_request_repo: IPlanRequestRepository) -> None:
        self.plan_request_repo = plan_request_repo

    async def generate(self, plan_request: PlanRequest) -> PlanRequest:
        request_data = {
            "id": plan_request.id,
        }

        await asyncio.to_thread(generate_plan_celery_task.delay, request_data)

        plan_request.status = PlanRequestStatus.PENDING

        result = await self.plan_request_repo.update(
            PlanRequestUpdateDTO(id=plan_request.id, status=PlanRequestStatus.PENDING)
        )

        return result
