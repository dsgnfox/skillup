from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.step import Step
from src.domain.models.user import UserID
from src.domain.ports.step_repository import IStepRepository
from src.infra.db.tables.steps import steps_table


class SQLAlchemyStepRepository(IStepRepository):
    """Репозиторий шагов плана обучения"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_many(self, steps: List[Step]) -> List[Step]:
        """Создать шаги плана обучения"""
        self._session.add_all(steps)
        await self._session.flush()
        return steps

    async def get_all_by_user_id(self, user_id: UserID) -> List[Step]:
        """Получить все шаги пользователя"""
        stmt = select(Step).where(steps_table.c.user_id == user_id)
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
