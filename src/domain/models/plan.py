from dataclasses import dataclass
from enum import Enum
import uuid

from src.domain.models.user import UserID


class PlanStatus(int, Enum):
    DRAFT = 10  # Ожидает старта
    IN_PROGRESS = 50  # Пользователь начал обучение (активен)
    COMPLETED = 100  # Завершён


@dataclass
class Plan:
    """Модель плана обучения"""

    id: uuid.UUID
    name: str
    user_id: UserID
    status: PlanStatus
