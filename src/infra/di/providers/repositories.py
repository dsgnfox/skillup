from dishka import Provider, Scope, provide

from src.domain.ports.plan_repository import IPlanRepository
from src.domain.ports.plan_request_repository import IPlanRequestRepository
from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.domain.ports.user_repository import IUserRepository
from src.infra.repositories.plan_repository import SQLAlchemyPlanRepository
from src.infra.repositories.plan_request_repository import (
    SQLAlchemyPlanRequestRepository,
)
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
    plan_repo = provide(SQLAlchemyPlanRepository, provides=IPlanRepository)
    plan_requests_repo = provide(
        SQLAlchemyPlanRequestRepository, provides=IPlanRequestRepository
    )
