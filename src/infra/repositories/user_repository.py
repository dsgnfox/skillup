from sqlalchemy.ext.asyncio import (
    AsyncSession,
)
from src.domain.models.user import User
from src.domain.ports.user_repository import IUserRepository


class SQLAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, user: User) -> None:
        self.session.add(user)
        await self.session.flush()
