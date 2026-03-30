import pytest
from unittest.mock import AsyncMock
from src.application.commands.user_register_via_telegram import (
    RegisterUserViaTelegramCommand,
    RegisterUserViaTelegramPayload,
)
from src.domain.exceptions.telegram_already_added import TelegramAlreadyAdded


@pytest.mark.asyncio
async def test_execute_raises_exception_if_user_exists():
    """Тест проверки существования пользователя телеграм"""

    # Arrange
    tg_user_repo = AsyncMock()
    tg_user_repo.exists.return_value = True

    command = RegisterUserViaTelegramCommand(
        user_repo=AsyncMock(), tg_user_repo=tg_user_repo, event_bus=AsyncMock()
    )

    payload = RegisterUserViaTelegramPayload(telegram_id=123, first_name="Ivan")

    # Act & Assert
    with pytest.raises(TelegramAlreadyAdded):
        await command.execute(payload)

    tg_user_repo.exists.assert_awaited_once_with(123)
