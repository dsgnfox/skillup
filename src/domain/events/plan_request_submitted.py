from dataclasses import dataclass
from src.domain.events.base_event import BaseDomainEvent
from src.domain.models.plan_request import PlanRequest


@dataclass(frozen=True)
class PlanRequestSubmittedEvent(BaseDomainEvent):
    """Событие принятия в обработку запроса на создание плана обучения"""

    plan_request: PlanRequest
