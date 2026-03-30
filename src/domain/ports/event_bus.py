from typing import Awaitable, Callable, Protocol, Type

from src.domain.events.base_event import BaseDomainEvent


class IEventBus(Protocol):
    """Протокол шины событий"""

    def subscribe(
        self, event_type: Type[BaseDomainEvent], handler: Awaitable[Callable]
    ) -> None:
        """Подписаться на событие"""
        ...

    async def publish(self, event: BaseDomainEvent) -> None:
        """Опубликовать событие"""
        ...
