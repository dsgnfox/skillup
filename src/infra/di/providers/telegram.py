from aiogram import Bot
from dishka import Provider, Scope, provide
from src.infra.config.telegram import TelegramSettings
from src.infra.views.telegram.controller import TelegramController


class TelegramProvider(Provider):
    @provide(scope=Scope.APP)
    def bot(self, config_telegram: TelegramSettings) -> Bot:
        return Bot(token=config_telegram.bot_token.get_secret_value())

    @provide(scope=Scope.APP)
    def controller(self, bot: Bot) -> TelegramController:
        return TelegramController(bot)
