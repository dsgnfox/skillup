from abc import ABC
from dataclasses import dataclass


@dataclass(frozen=True)
class BaseDomainEvent(ABC):
    """Базовый класс для всех доменных событий."""

    pass
