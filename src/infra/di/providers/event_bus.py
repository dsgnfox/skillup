from typing import AsyncGenerator, Type

from dishka import Provider, Scope, provide, AsyncContainer
from src.application.event_handlers.plan_request_submitted import (
    PlanRequestSubmittedHandler,
)
from src.domain.events.base_event import BaseDomainEvent
from src.domain.events.plan_request_submitted import PlanRequestSubmittedEvent
from src.domain.ports.event_bus import IEventBus, IHandlerFactory
from src.infra.config.settings import Settings
from src.infra.event_bus.dishka_handler_factory import DishkaHandlerFactory
from src.infra.event_bus.redis import RedisEventBus
from src.infra.logger import ILogger

EVENT_SUBSCRIBERS: list[tuple[Type[BaseDomainEvent], Type]] = [
    (PlanRequestSubmittedEvent, PlanRequestSubmittedHandler),
]


class EventBusProvider(Provider):
    scope = Scope.APP

    @provide
    def get_factory(self, container: AsyncContainer) -> IHandlerFactory:
        return DishkaHandlerFactory(container)

    @provide
    async def get_event_bus(
        self, factory: IHandlerFactory, logger: ILogger, settings: Settings
    ) -> AsyncGenerator[IEventBus, None]:
        bus = RedisEventBus(handler_factory=factory, logger=logger)

        if not settings.is_celery_worker:
            for event_type, handler_cls in EVENT_SUBSCRIBERS:
                bus.subscribe(event_type, handler_cls)

        await bus.init()
        yield bus
        await bus.close()
