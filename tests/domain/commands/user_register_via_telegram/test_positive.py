from unittest.mock import AsyncMock

from src.application.commands.user_register_via_telegram import (
    RegisterUserViaTelegramCommand,
    RegisterUserViaTelegramPayload,
)
from src.domain.events.user_register import UserRegisterEvent


async def test_execute_success_registration():
    """Тест успешной регистрации пользователя через телеграм"""

    # Arrange
    user_repo = AsyncMock()
    tg_user_repo = AsyncMock()
    event_bus = AsyncMock()

    tg_user_repo.exists.return_value = False

    command = RegisterUserViaTelegramCommand(
        user_repo=user_repo, tg_user_repo=tg_user_repo, event_bus=event_bus
    )

    payload = RegisterUserViaTelegramPayload(
        telegram_id=123, first_name="Ivan", username="ivan_boss"
    )

    # Act
    result_user = await command.execute(payload)

    # Assert
    # 1. Проверка сохранения основного пользователя
    user_repo.save.assert_awaited_once()
    saved_user = user_repo.save.call_args[0][0]
    assert saved_user.name == "Ivan"

    # 2. Проверка сохранения связи с Telegram
    tg_user_repo.save.assert_awaited_once()
    saved_tg_user = tg_user_repo.save.call_args[0][0]
    assert saved_tg_user.telegram_id == 123
    assert saved_tg_user.user_id == result_user.id
    assert saved_tg_user.username == "ivan_boss"

    # 3. Проверка публикации события
    event_bus.publish.assert_awaited_once()
    event = event_bus.publish.call_args[0][0]
    assert isinstance(event, UserRegisterEvent)
    # assert event.user == result_user # fixme

    # 4. Проверка возвращаемого значения
    assert result_user.name == "Ivan"
