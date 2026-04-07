from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Protocol, Type

from src.domain.events.base_event import BaseDomainEvent


class IEventBus(Protocol):
    """Протокол шины событий"""

    def subscribe(self, event_type: Type[BaseDomainEvent], handler_cls: Type) -> None:
        """Подписаться на событие"""
        ...

    async def publish(self, event: BaseDomainEvent) -> None:
        """Опубликовать событие"""
        ...


class IHandlerFactory(Protocol):
    """
    Протокол фабрики, которая умеет создавать обработчики событий
    в рамках изолированного Scope.REQUEST.
    """

    @asynccontextmanager
    def create_handler(self, handler_cls: Type) -> AsyncIterator[Any]:
        """Создать обработчик события из переданного типа"""
        ...
