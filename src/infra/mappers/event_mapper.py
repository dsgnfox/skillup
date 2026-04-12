from dataclasses import asdict
from typing import Type, TypeVar, Any, Dict
from datetime import datetime
from uuid import UUID
from dacite import from_dict, Config
from src.domain.events.base_event import BaseDomainEvent
from src.domain.models.plan import PlanStatus
from src.domain.models.plan_request import PlanRequestStatus
from src.domain.models.step import StepStatus
from src.infra.exceptions.event_mapper_exception import EventMapperException


T = TypeVar("T", bound=BaseDomainEvent)


class EventMapper:
    @staticmethod
    def to_dict(event: BaseDomainEvent) -> Dict[str, Any]:
        """Сериализация наследников BaseDomainEvent в словарь."""

        if not isinstance(event, BaseDomainEvent):
            raise EventMapperException(
                f"Объект {type(event)} должен наследоваться от BaseDomainEvent"
            )
        try:
            return asdict(event)
        except Exception as e:
            raise EventMapperException(f"Ошибка при преобразовании в dict: {e}")

    @staticmethod
    def from_dict(data: Dict[str, Any], event_class: Type[T]) -> T:
        """Десериализация словаря в конкретный класс события."""

        try:
            return from_dict(
                data_class=event_class,
                data=data,
                config=Config(
                    type_hooks={
                        datetime: datetime.fromisoformat,
                        UUID: UUID,
                        PlanRequestStatus: PlanRequestStatus,
                        StepStatus: StepStatus,
                        PlanStatus: PlanStatus,
                    }
                ),
            )
        except Exception as e:
            raise EventMapperException(
                f"Не удалось восстановить событие {event_class.__name__}: {e}"
            )
