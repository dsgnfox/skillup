from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
import uuid

UserID: TypeAlias = uuid.UUID


@dataclass
class User:
    id: UserID
    name: str
    created_at: datetime
    is_active: bool

    @staticmethod
    def create(name: str) -> "User":
        return User(
            id=uuid.uuid7(), name=name, created_at=datetime.now(), is_active=True
        )
