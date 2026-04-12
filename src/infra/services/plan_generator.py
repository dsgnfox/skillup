import asyncio
from celery import Celery
from src.domain.models.plan_request import PlanRequest, PlanRequestStatus
from src.domain.ports.dto.plan_request_update_dto import PlanRequestUpdateDTO
from src.domain.ports.plan_generator import IPlanGeneratorService
from src.domain.ports.plan_request_repository import IPlanRequestRepository
from src.infra.logger import ILogger


class PlanGeneratorService(IPlanGeneratorService):
    """Сервис для генерации учебного плана"""

    def __init__(
        self, plan_request_repo: IPlanRequestRepository, celery: Celery, logger: ILogger
    ) -> None:
        self._plan_request_repo = plan_request_repo
        self._celery = celery
        self._logger = logger.createScope(self.__class__.__name__)

    async def generate(self, plan_request: PlanRequest) -> PlanRequest:
        request_data = {
            "id": plan_request.id,
            "request": plan_request.request,
            "user_id": str(plan_request.user_id),
        }

        self._logger.info("plan request data", {"request_data": request_data})

        await asyncio.to_thread(
            self._celery.send_task,
            "tasks.generate_plan_celery_task",
            args=[request_data],
        )

        result = await self._plan_request_repo.update(
            PlanRequestUpdateDTO(
                id=plan_request.id,
                request=plan_request.request,
                status=PlanRequestStatus.PROCESSING,
            )
        )

        self._logger.info("plan generator result", {"result": result})

        return result
