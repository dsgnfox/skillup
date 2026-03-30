from dataclasses import dataclass
from enum import Enum
import uuid

from src.domain.models.user import UserID


class PlanStatus(Enum):
    PROCESS_CREATION = 1
    IN_PROGRESS = 2
    COMPLETED = 100


@dataclass
class Plan:
    """Модель плана обучения"""

    id: uuid.UUID
    name: str
    user_id: UserID
    status: PlanStatus
