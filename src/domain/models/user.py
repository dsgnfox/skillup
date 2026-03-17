from dataclasses import dataclass
from datetime import datetime
import uuid

type UserID = uuid.UUID


@dataclass
class User:
    id: UserID
    name: str
    created_at: datetime
    is_active: bool
