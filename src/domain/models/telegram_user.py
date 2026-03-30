from dataclasses import dataclass
from typing import Optional
import uuid
from .user import UserID


@dataclass
class TelegramUser:
    id: uuid.UUID
    telegram_id: int
    first_name: str
    user_id: UserID
    username: Optional[str] = None
    last_name: Optional[str] = None
