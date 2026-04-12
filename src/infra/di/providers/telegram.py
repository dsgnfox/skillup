from aiogram import Bot
from dishka import Provider, Scope, provide
from src.infra.config.telegram import TelegramSettings
from src.infra.views.telegram.plan_create.plan_create_controller import (
    TelegramControllerPlanCreate,
)
from src.infra.views.telegram.start.start_controller import TelegramControllerStart


class TelegramProvider(Provider):
    @provide(scope=Scope.APP)
    def bot(self, config_telegram: TelegramSettings) -> Bot:
        return Bot(token=config_telegram.bot_token.get_secret_value())

    @provide(scope=Scope.APP)
    def controller_start(self, bot: Bot) -> TelegramControllerStart:
        return TelegramControllerStart(bot)

    @provide(scope=Scope.APP)
    def controller(self, bot: Bot) -> TelegramControllerPlanCreate:
        return TelegramControllerPlanCreate(bot)
