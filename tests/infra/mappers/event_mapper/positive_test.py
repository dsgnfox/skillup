import uuid

import pytest
from uuid import uuid4, UUID
from datetime import datetime
from dataclasses import dataclass
from src.domain.events.base_event import BaseDomainEvent
from src.domain.events.plan_request_submitted import PlanRequestSubmittedEvent
from src.domain.models.plan import PlanStatus
from src.domain.models.plan_request import PlanRequestStatus
from src.domain.models.step import StepStatus
from src.domain.models.user import UserID
from src.infra.mappers.event_mapper import EventMapper


# Сущности для теста вложенности
@dataclass(frozen=True)
class Level3(BaseDomainEvent):
    value: str


@dataclass(frozen=True)
class Level2(BaseDomainEvent):
    nested: Level3


@dataclass(frozen=True)
class Level1(BaseDomainEvent):
    nested: Level2


# Базовые тестовые сущности
@dataclass(frozen=True)
class SimpleEvent(BaseDomainEvent):
    id: str


@dataclass(frozen=True)
class ComplexEvent(BaseDomainEvent):
    event_id: UUID
    created_at: datetime
    payload: str


def test_to_dict_positive_simple():
    """Проверка корректной сериализации простого датакласса в словарь"""
    event = SimpleEvent(id="123")
    result = EventMapper.to_dict(event)
    assert result == {"id": "123"}


def test_to_dict_positive_with_uuid_and_datetime():
    """Проверка сериализации объектов UUID и datetime (должны остаться объектами перед json.dumps)"""
    u = uuid4()
    now = datetime.now()
    event = ComplexEvent(event_id=u, created_at=now, payload="test")
    result = EventMapper.to_dict(event)

    assert result["event_id"] == u
    assert result["created_at"] == now


def test_from_dict_positive_with_PlanRequestSubmittedEvent():
    """Проверка десериализации из словаря событие с user id"""
    data = {
        "plan_request": {
            "id": "019d8146-3106-7537-a568-024784e10136",
            "user_id": "019d7d89-21f3-737a-b4d4-d23bf17506e3",
            "status": 0,
            "request": "играть на гитаре",
            "created_at": "2026-04-12 13:39:14.182400",
            "updated_at": None,
            "plan_id": None,
            "error_msg": None,
        }
    }
    event = EventMapper.from_dict(data, PlanRequestSubmittedEvent)

    assert isinstance(event.plan_request.user_id, uuid.UUID)
    assert isinstance(event.plan_request.status, PlanRequestStatus)


def test_from_dict_positive_with_enums():
    """Проверка десериализации из словаря событие с user id"""

    @dataclass(frozen=True)
    class EventEnum(BaseDomainEvent):
        plan_request_status: PlanRequestStatus
        step_status: StepStatus
        plan_status: PlanStatus

    data = {
        "plan_request_status": 10,
        "step_status": 50,
        "plan_status": 100,
    }
    event = EventMapper.from_dict(data, EventEnum)

    assert isinstance(event.plan_request_status, PlanRequestStatus)
    assert event.plan_request_status == PlanRequestStatus.PROCESSING

    assert isinstance(event.step_status, StepStatus)
    assert event.step_status == StepStatus.IN_PROGRESS

    assert isinstance(event.plan_status, PlanStatus)
    assert event.plan_status == PlanStatus.COMPLETED


def test_from_dict_positive_complex():
    """Проверка десериализации из словаря со строками в объекты UUID и datetime"""
    u = uuid4()
    now = datetime.now()
    data = {
        "event_id": str(u),
        "created_at": now.isoformat(),
        "payload": "data",
    }
    event = EventMapper.from_dict(data, ComplexEvent)

    assert isinstance(event.event_id, UUID)
    assert isinstance(event.created_at, datetime)
    assert event.event_id == u


def test_nested_dataclasses_three_levels():
    """Проверка корректной обработки вложенных структур до 3-го уровня включительно"""
    data = {"nested": {"nested": {"value": "deep_val"}}}
    event = EventMapper.from_dict(data, Level1)

    assert isinstance(event.nested, Level2)
    assert isinstance(event.nested.nested, Level3)
    assert event.nested.nested.value == "deep_val"

    # Обратный маппинг
    dict_back = EventMapper.to_dict(event)
    assert dict_back == data
