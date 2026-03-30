from pydantic import BaseModel, Field, SecretStr


class TelegramSettings(BaseModel):
    """Настройки для телеграм"""

    bot_token: SecretStr = Field(min_length=1)
