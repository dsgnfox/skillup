from dataclasses import dataclass
import uuid
from src.domain.events.base_event import BaseDomainEvent
from src.domain.models.plan_request import PlanRequest


@dataclass(frozen=True)
class PlanCreationCompleteEvent(BaseDomainEvent):
    """Событие завершения создания плана обучения"""

    plan_request_id: uuid.UUID
