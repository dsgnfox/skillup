from dataclasses import dataclass
from src.domain.events.base_event import BaseDomainEvent
from src.domain.models.user import User


@dataclass(frozen=True)
class UserRegisterEvent(BaseDomainEvent):
    """Событие регистрации пользователя"""

    user: User
