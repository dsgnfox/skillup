from dataclasses import dataclass
from enum import Enum
import uuid

from src.domain.models.user import UserID


class StepStatus(Enum):
    IN_PROGRESS = 2
    COMPLETED = 100


@dataclass
class Step:
    """Модель шага плана обучения"""

    id: uuid.UUID
    name: str
    content: str
    status: StepStatus
    user_id: UserID
