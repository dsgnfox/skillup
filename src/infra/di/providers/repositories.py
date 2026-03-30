from dishka import Provider, Scope, provide

from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.domain.ports.user_repository import IUserRepository
from src.infra.repositories.telegram_user_repository import (
    SQLAlchemyTelegramUserRepository,
)
from src.infra.repositories.user_repository import SQLAlchemyUserRepository


class RepositoriesProvider(Provider):
    """Провайдер репозиториев"""

    scope = Scope.REQUEST

    user_repo = provide(SQLAlchemyUserRepository, provides=IUserRepository)
    tg_user_repo = provide(
        SQLAlchemyTelegramUserRepository, provides=ITelegramUserRepository
    )
