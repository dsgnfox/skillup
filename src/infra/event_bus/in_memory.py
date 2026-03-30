from typing import Callable, Dict, List, Type

from src.domain.events.base_event import BaseDomainEvent
from src.domain.ports.event_bus import IEventBus


class InMemoryEventBus(IEventBus):
    def __init__(self):
        self._handlers: Dict[Type[BaseDomainEvent], List[Callable]] = {}

    def subscribe(self, event_type: Type[BaseDomainEvent], handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: BaseDomainEvent) -> None:
        event_type = type(event)
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                await handler(event)
