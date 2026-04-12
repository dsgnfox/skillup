from dishka import Provider, Scope, provide

from src.infra.config.ai import AiConfig
from src.infra.config.database import DatabaseConfig
from src.infra.config.settings import Settings
from src.infra.config.telegram import TelegramSettings


class SettingsProvider(Provider):
    """Провайдер настроек"""

    scope = Scope.APP

    @provide
    def get_settings(self) -> Settings:
        return Settings()  # type: ignore

    @provide
    def get_settings_database(self, config: Settings) -> DatabaseConfig:
        return config.database

    @provide
    def get_settings_telegram(self, config: Settings) -> TelegramSettings:
        return config.telegram

    @provide
    def get_settings_ai(self, config: Settings) -> AiConfig:
        return config.ai
