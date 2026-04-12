from sqlalchemy.orm import registry

from src.domain.models.plan import Plan
from src.domain.models.plan_request import PlanRequest
from src.domain.models.step import Step
from src.domain.models.telegram_user import TelegramUser
from src.domain.models.user import User

from src.infra.db.tables.telegram_users import telegram_users_table
from src.infra.db.tables.users import users_table
from src.infra.db.tables.plans import plans_table
from src.infra.db.tables.plan_requests import plan_requests_table
from src.infra.db.tables.steps import steps_table


mapper_registry = registry()


def start_mappers():
    mapper_registry.map_imperatively(TelegramUser, telegram_users_table)
    mapper_registry.map_imperatively(User, users_table)
    mapper_registry.map_imperatively(Plan, plans_table)
    mapper_registry.map_imperatively(PlanRequest, plan_requests_table)
    mapper_registry.map_imperatively(Step, steps_table)
