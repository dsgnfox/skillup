import asyncio
import json
from typing import Dict, List, Type, Any
import redis.asyncio as redis
from redis.asyncio.client import PubSub
from src.domain.events.base_event import BaseDomainEvent
from src.domain.ports.event_bus import IEventBus, IHandlerFactory
from src.infra.event_bus.exception import RedisEventBusException
from src.infra.exceptions.event_mapper_exception import EventMapperException
from src.infra.logger import ILogger
from src.infra.mappers.event_mapper import EventMapper


class RedisEventBus(IEventBus):
    """Шина событий на базе Redis Pub/Sub с поддержкой DI-фабрики."""

    def __init__(
        self,
        handler_factory: IHandlerFactory,
        logger: ILogger,
        redis_url: str = "redis://localhost:6379/1",
    ):
        self._logger = logger.createScope(self.__class__.__name__)
        self._redis_url = redis_url
        self._factory = handler_factory

        self._redis: redis.Redis | None = None
        self._pubsub: PubSub | None = None

        # Храним классы хэндлеров: { "ИмяСобытия": [КлассХэндлера1, ...] }
        self._handlers: Dict[str, List[Type]] = {}

        # Реестр классов событий для десериализации: { "ИмяСобытия": КлассСобытия }
        self._event_types: Dict[str, Type[BaseDomainEvent]] = {}

        self._listen_task: asyncio.Task | None = None

        self._logger.debug("Инициализация")

    async def init(self) -> None:
        self._redis = redis.from_url(self._redis_url)
        self._pubsub = self._redis.pubsub()
        # НЕ запускаем здесь loop сразу
        self._logger.debug("Соединение с Redis установлено")

    async def start_listening(self) -> None:
        """Отдельный метод для запуска цикла"""
        if self._handlers and self._pubsub:
            # Подписываемся ДО запуска цикла
            await self._pubsub.subscribe(*self._handlers.keys())

        self._listen_task = asyncio.create_task(self._listen_loop())
        self._logger.debug("Цикл прослушивания запущен")

    async def close(self) -> None:
        """
        Корректно останавливает фоновую задачу и закрывает соединения.
        """
        if self._listen_task:
            self._listen_task.cancel()
            try:
                await self._listen_task
            except asyncio.CancelledError:
                pass

        if self._pubsub:
            await self._pubsub.close()
        if self._redis:
            await self._redis.close()

        self._logger.debug("Сервис остановлен")

    async def subscribe(
        self, event_type: Type[BaseDomainEvent], handler_cls: Type
    ) -> None:
        """Регистрирует класс обработчика для события."""

        channel_name = event_type.__name__

        if channel_name not in self._handlers:
            self._handlers[channel_name] = []
            self._event_types[channel_name] = event_type

            # Динамически подписываемся в Redis, если цикл уже запущен
            if self._pubsub:
                await self._pubsub.subscribe(channel_name)

        self._handlers[channel_name].append(handler_cls)
        self._logger.debug(
            "Новый подписчик",
            {"event_type": event_type.__name__, "handler_cls": handler_cls.__name__},
        )

    async def publish(self, event: BaseDomainEvent) -> None:
        """Публикует событие в Redis, используя EventMapper."""
        if not self._redis:
            raise RedisEventBusException(
                "RedisEventBus не инициализирован. Вызовите init()."
            )

        try:
            channel_name = event.__class__.__name__
            dict_data = EventMapper.to_dict(event)
            event_data = json.dumps(dict_data, default=str)

            await self._redis.publish(channel_name, event_data)
            self._logger.debug(
                "Новое событие опубликовано",
                {"event": channel_name, "event_data": event_data},
            )
        except EventMapperException as e:
            raise RedisEventBusException(f"Ошибка маппинга при публикации: {e}")
        except Exception as e:
            raise RedisEventBusException(f"Ошибка при публикации в Redis: {e}")

    async def _listen_loop(self) -> None:
        """Бесконечный цикл чтения сообщений с использованием идиоматичного listen()"""

        if self._pubsub is None:
            raise RedisEventBusException("PubSub не инициализирован")

        try:
            # Сначала подписываемся на те каналы, которые уже успели зарегистрировать
            if self._handlers:
                await self._pubsub.subscribe(*self._handlers.keys())

            async for message in self._pubsub.listen():
                if message["type"] == "message":
                    await self._process_message(message)
        except asyncio.CancelledError:
            self._logger.info("[Redis EventBus] Фоновая задача остановлена.")
        except Exception as e:
            raise RedisEventBusException(
                "Критическая ошибка в цикле прослушивания: {e}"
            )

    async def _process_message(self, message: dict) -> None:
        """Обработка сообщения с десериализацией через EventMapper."""

        channel_name = message["channel"].decode("utf-8")
        data_str = message["data"].decode("utf-8")

        handler_classes = self._handlers.get(channel_name, [])
        event_cls = self._event_types.get(channel_name)

        if not handler_classes or not event_cls:
            return

        try:
            event_dict = json.loads(data_str)
            event_instance = EventMapper.from_dict(event_dict, event_cls)

            for handler_cls in handler_classes:
                asyncio.create_task(self._run_handler(handler_cls, event_instance))

        except EventMapperException as e:
            self._logger.error(f"Ошибка восстановления события {channel_name}: {e}")
        except json.JSONDecodeError as e:
            self._logger.error(f"Невалидный JSON в канале {channel_name}: {e}")
        except Exception as e:
            self._logger.error(f"Непредвиденная ошибка при обработке сообщения: {e}")

    async def _run_handler(self, handler_cls: Type, event: Any) -> None:
        """
        Запускает конкретный хэндлер в своем собственном Scope.REQUEST через фабрику.
        """

        try:
            async with self._factory.create_handler(handler_cls) as handler:
                await handler.handle(event)

        except Exception as e:
            raise RedisEventBusException(
                f"Ошибка в обработчике события {handler_cls.__name__}: {e}"
            )
