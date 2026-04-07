from dataclasses import dataclass
from typing import Optional, Protocol
from uuid import uuid7
from src.application.commands.base_command import BaseCommand
from src.domain.events.user_register import UserRegisterEvent
from src.domain.exceptions.telegram_already_added import TelegramAlreadyAdded
from src.domain.models.telegram_user import TelegramUser
from src.domain.models.user import User
from src.domain.ports.event_bus import IEventBus
from src.domain.ports.telegram_user_repository import ITelegramUserRepository
from src.domain.ports.user_repository import IUserRepository


@dataclass
class RegisterUserViaTelegramPayload:
    telegram_id: int
    first_name: str
    username: Optional[str] = None


class IRegisterUserViaTelegramCommand(Protocol):
    async def execute(self, payload: RegisterUserViaTelegramPayload) -> User: ...


class RegisterUserViaTelegramCommand(BaseCommand):
    """Команда регистрации пользователя с помощью телеграм"""

    def __init__(
        self,
        user_repo: IUserRepository,
        tg_user_repo: ITelegramUserRepository,
        event_bus: IEventBus,
    ):
        self.user_repo = user_repo
        self.tg_user_repo = tg_user_repo
        self.event_bus = event_bus

    async def execute(self, payload: RegisterUserViaTelegramPayload) -> User:
        if await self.tg_user_repo.exists(payload.telegram_id):
            raise TelegramAlreadyAdded()

        user = User.create(name=payload.first_name)
        await self.user_repo.save(user)

        tg_user = TelegramUser(
            id=uuid7(),
            telegram_id=payload.telegram_id,
            user_id=user.id,
            first_name=payload.first_name,
            username=payload.username,
        )
        await self.tg_user_repo.save(tg_user)

        await self.event_bus.publish(
            UserRegisterEvent(
                user_id=user.id,
                name=user.name,
                created_at=user.created_at,
                is_active=user.is_active,
            )
        )

        return user
