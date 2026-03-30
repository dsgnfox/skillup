from sqlalchemy.orm import registry

from src.domain.models.telegram_user import TelegramUser
from src.domain.models.user import User

from src.infra.db.tables.telegram_users import telegram_users_table
from src.infra.db.tables.users import users_table


mapper_registry = registry()


def start_mappers():
    mapper_registry.map_imperatively(TelegramUser, telegram_users_table)
    mapper_registry.map_imperatively(User, users_table)
