from importlib.metadata import metadata
from dishka import Provider, Scope, provide
from src.domain.ports.event_bus import IEventBus
from src.infra.config.settings import Settings
from src.infra.event_bus.in_memory import InMemoryEventBus
from src.infra.logger import ILogger, StdlibLogger


class InfrastructureProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_logger(self, settings: Settings) -> ILogger:
        return StdlibLogger(settings.name)
