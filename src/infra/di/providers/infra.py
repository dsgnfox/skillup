from dishka import Provider, Scope, provide

from src.domain.ports.event_bus import IEventBus
from src.infra.event_bus.in_memory import InMemoryEventBus


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_event_bus(self) -> IEventBus:
        return InMemoryEventBus()
