from contextlib import asynccontextmanager
from typing import AsyncIterator, Type, Any
from dishka import AsyncContainer
from src.domain.ports.event_bus import IHandlerFactory


class DishkaHandlerFactory(IHandlerFactory):
    def __init__(self, container: AsyncContainer):
        self._container = container

    @asynccontextmanager
    async def create_handler(self, handler_cls: Type) -> AsyncIterator[Any]:
        async with self._container() as request_container:
            handler = await request_container.get(handler_cls)
            yield handler
