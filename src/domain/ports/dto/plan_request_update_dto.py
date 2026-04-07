from dataclasses import dataclass, fields
from typing import Optional
import uuid

from src.domain.models.plan_request import PlanRequestStatus


@dataclass
class PlanRequestUpdateDTO:
    """DTO для обновления запроса на создание плана обучения"""

    id: uuid.UUID
    status: Optional[PlanRequestStatus]
    plan_id: Optional[uuid.UUID] = None
    error_msg: Optional[str] = None

    def __iter__(self):
        for field in fields(self):
            yield field.name, getattr(self, field.name)
