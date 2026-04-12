from dataclasses import dataclass
from datetime import datetime
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
    created_at: datetime

    @staticmethod
    def create(
        title: str, description: str, user_id: UserID, plan_id: uuid.UUID
    ) -> "Step":
        return Step(
            id=uuid.uuid7(),
            name=title,
            content=description,
            status=StepStatus.DRAFT,
            user_id=user_id,
            plan_id=plan_id,
            created_at=datetime.now(),
        )
