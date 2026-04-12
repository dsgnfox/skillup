from aiogram import Bot
from celery import Celery
from dishka import Provider, Scope, provide
from src.domain.ports.plan_generator import IPlanGeneratorService
from src.domain.ports.plan_request_repository import IPlanRequestRepository
from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.domain.ports.user_notifier import IUserNotifier
from src.infra.config.settings import Settings
from src.infra.logger import ILogger, StdlibLogger
from src.infra.notifiers.telegram_notifier import TelegramNotifier
from src.infra.services.plan_generator import PlanGeneratorService
from src.infra.celery_app import celery_app


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_logger(self, settings: Settings) -> ILogger:
        return StdlibLogger(settings.name)

    @provide(scope=Scope.REQUEST)
    def provide_notifier(
        self, bot: Bot, telegram_user_repo: ITelegramUserRepository
    ) -> IUserNotifier:
        return TelegramNotifier(bot, telegram_user_repo)

    @provide(scope=Scope.REQUEST)
    def provide_plan_generator_service(
        self, plan_request_repo: IPlanRequestRepository, celery: Celery, logger: ILogger
    ) -> IPlanGeneratorService:
        return PlanGeneratorService(plan_request_repo, celery, logger)

    @provide(scope=Scope.APP)
    def provide_celery(self) -> Celery:
        return celery_app
