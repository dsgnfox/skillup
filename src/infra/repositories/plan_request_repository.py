from datetime import datetime
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.plan_request import PlanRequest
from src.domain.models.user import UserID
from src.domain.ports.dto.plan_request_update_dto import PlanRequestUpdateDTO
from src.domain.ports.plan_request_repository import IPlanRequestRepository
from src.infra.db.tables.plan_requests import plan_requests_table
from src.infra.repositories.exception import NotFoundElement


class SQLAlchemyPlanRequestRepository(IPlanRequestRepository):
    """Репозиторий запросов на создание планов обучения"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, plan_request: PlanRequest) -> PlanRequest:
        self._session.add(plan_request)
        await self._session.flush()
        return plan_request

    async def update(self, plan_request_dto: PlanRequestUpdateDTO) -> PlanRequest:
        stmt = select(PlanRequest).where(
            plan_requests_table.c.id == plan_request_dto.id
        )
        result = await self._session.execute(stmt)
        plan_request = result.scalar_one()

        if plan_request is None:
            raise NotFoundElement()

        for field_name, field_value in plan_request_dto:
            if field_value is not None:
                setattr(plan_request, field_name, field_value)

        plan_request.updated_at = datetime.now()

        await self._session.flush()
        return plan_request

    async def get_all_by_user_id(self, user_id: UserID) -> list[PlanRequest]:
        stmt = select(PlanRequest).where(plan_requests_table.c.user_id == user_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, id: uuid.UUID) -> PlanRequest | None:
        stmt = select(PlanRequest).where(plan_requests_table.c.id == id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
