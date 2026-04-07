from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.models.telegram_user import TelegramUser
from src.domain.models.user import UserID
from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.infra.db.tables.telegram_users import telegram_users_table


class SQLAlchemyTelegramUserRepository(ITelegramUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[TelegramUser]:
        stmt = select(TelegramUser).where(
            telegram_users_table.c.telegram_id == telegram_id
        )
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_user_id(self, user_id: UserID) -> Optional[TelegramUser]:
        stmt = select(TelegramUser).where(telegram_users_table.c.user_id == user_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def save(self, telegram_user: TelegramUser) -> None:
        self._session.add(telegram_user)
        await self._session.flush()

    async def exists(self, telegram_id: int) -> bool:
        stmt = select(
            select(TelegramUser)
            .where(telegram_users_table.c.telegram_id == telegram_id)
            .exists()
        )
        result = await self._session.execute(stmt)
        return result.scalar() or False
