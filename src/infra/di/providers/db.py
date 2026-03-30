from typing import AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)

from src.infra.config.database import DatabaseConfig
from src.infra.db.mapper import start_mappers


class DatabaseProvider(Provider):
    """Провайдер базы данных"""

    @provide(scope=Scope.APP)
    def provide_engine(self, db_config: DatabaseConfig) -> AsyncEngine:
        start_mappers()

        return create_async_engine(
            url=db_config.async_url,
            echo=db_config.sqla.echo,
            pool_size=db_config.sqla.pool_size,
            max_overflow=db_config.sqla.max_overflow,
        )

    @provide(scope=Scope.REQUEST)
    async def provide_session(self, engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
        maker = async_sessionmaker(engine, expire_on_commit=False)
        async with maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
