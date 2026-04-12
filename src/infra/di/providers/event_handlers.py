from dishka import Provider, Scope, provide

from src.application.event_handlers.plan_creation_complete import (
    PlanCreationCompleteHandler,
)
from src.application.event_handlers.plan_request_submitted import (
    PlanRequestSubmittedHandler,
)


class EventHandlerProvider(Provider):
    """Провайдер обработчиков событий"""

    scope = Scope.REQUEST

    plan_request_submitted = provide(PlanRequestSubmittedHandler)
    plan_creation_complete = provide(PlanCreationCompleteHandler)
