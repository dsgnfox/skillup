from src.infra.di.providers.commands import CommandProvider
from src.infra.di.providers.config import ConfigProvider
from src.infra.di.providers.db import DatabaseProvider
from src.infra.di.providers.infra import InfrastructureProvider
from src.infra.di.providers.repositories import RepositoriesProvider
from src.infra.di.providers.telegram import TelegramProvider


providers = (
    CommandProvider(),
    TelegramProvider(),
    DatabaseProvider(),
    ConfigProvider(),
    RepositoriesProvider(),
    InfrastructureProvider(),
)
