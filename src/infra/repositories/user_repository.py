from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from src.domain.models.user import User
from src.domain.ports.user_repository import IUserRepository
from src.infra.logger import ILogger


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, logger: ILogger, session: AsyncSession):
        self._logger = logger.createScope(self.__class__.__name__)
        self._session = session

    async def save(self, user: User) -> None:
        self._session.add(user)
        await self._session.flush()
