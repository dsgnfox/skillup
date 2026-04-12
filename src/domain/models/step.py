from dataclasses import dataclass
from enum import Enum
import uuid

from src.domain.models.user import UserID


class StepStatus(int, Enum):
    DRAFT = 10  # Ожидает старта
    IN_PROGRESS = 50  # Пользователь начал обучение (активен)
    COMPLETED = 100  # Завершён


@dataclass
class Step:
    """Модель шага плана обучения"""

    id: uuid.UUID
    name: str
    content: str
    status: StepStatus
    user_id: UserID
    plan_id: uuid.UUID
