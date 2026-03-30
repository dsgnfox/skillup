import os
from pathlib import Path

from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    PydanticBaseSettingsSource,
)

from src.infra.config.database import DatabaseConfig
from src.infra.config.telegram import TelegramSettings

CONFIG_DIR = Path.cwd()
ENVS_DIR = CONFIG_DIR / "envs"


app_env = os.getenv("APP_ENV", "dev")
print("=" * 20)
print(ENVS_DIR, app_env)
print("=" * 20)


class Settings(BaseSettings):
    """Настройки приложения"""

    telegram: TelegramSettings
    database: DatabaseConfig

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="SKILLUP__",  # suffix: two underscore chars
        env_nested_delimiter="__",  # two underscore chars
        env_file=(
            ENVS_DIR / ".env.template",
            ENVS_DIR / f".env.{app_env}",
        ),
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            env_settings,
            dotenv_settings,
        )
