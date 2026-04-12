from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from src.domain.events.base_event import BaseDomainEvent


@dataclass(frozen=True)
class UserRegisterEvent(BaseDomainEvent):
    """Событие регистрации пользователя"""

    user_id: UUID
    name: str
    created_at: datetime
    is_active: bool
