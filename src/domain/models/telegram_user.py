from datetime import datetime
from dataclasses import dataclass
from typing import Optional
from .user import UserID


@dataclass(frozen=True)
class TelegramUser:
    telegram_id: int
    first_name: str
    user_id: Optional[UserID] = None
    username: Optional[str] = None
    last_name: Optional[str] = None
    is_premium: bool = False
    updated_at: datetime = datetime.now()
