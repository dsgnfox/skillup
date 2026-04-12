from dataclasses import dataclass
import uuid
from src.domain.events.base_event import BaseDomainEvent
from src.domain.models.user import UserID


@dataclass
class PlanCreationCompleteStep:
    title: str
    description: str


@dataclass(frozen=True)
class PlanCreationCompleteEvent(BaseDomainEvent):
    """Событие завершения создания плана обучения"""

    plan_request_id: uuid.UUID
    user_id: UserID
    steps: list[PlanCreationCompleteStep]
    is_success: bool
    error: str | None
