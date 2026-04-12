from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid

from src.domain.models.user import UserID


class PlanRequestStatus(int, Enum):
    PENDING = 0  # Запрос принят, ждёт обработки
    PROCESSING = 10  # Запрос в процессе обработки
    COMPLETED = 20  # Обработка запроса успешно завершена
    FAILED = 30  # Обработка запроса завершена с ошибкой


@dataclass
class PlanRequest:
    """Модель запроса на создание плана обучения"""

    id: uuid.UUID
    user_id: UserID
    status: PlanRequestStatus
    request: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    plan_id: Optional[uuid.UUID] = None
    error_msg: Optional[str] = None
