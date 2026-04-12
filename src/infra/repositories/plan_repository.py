from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.plan import Plan
from src.domain.models.user import UserID
from src.domain.ports.plan_repository import IPlanRepository
from src.infra.db.tables.plans import plans_table


class SQLAlchemyPlanRepository(IPlanRepository):
    """Репозиторий планов обучения"""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, plan: Plan) -> Plan:
        self._session.add(plan)
        await self._session.flush()
        return plan

    async def get_all_by_user_id(self, user_id: UserID) -> List[Plan]:
        stmt = select(Plan).where(plans_table.c.user_id == user_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
