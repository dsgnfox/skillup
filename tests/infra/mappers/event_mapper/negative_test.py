import pytest
from dataclasses import dataclass
from src.domain.events.base_event import BaseDomainEvent
from src.infra.exceptions.event_mapper_exception import EventMapperException
from src.infra.mappers.event_mapper import EventMapper


@dataclass
class NotABaseDomainEvent:
    id: str


@dataclass(frozen=True)
class SimpleEvent(BaseDomainEvent):
    id: str


def test_to_dict_negative_not_base_event():
    """Проверка выброса исключения, если объект не наследуется от BaseDomainEvent"""

    bad_obj = NotABaseDomainEvent(id="err")
    with pytest.raises(EventMapperException):
        EventMapper.to_dict(bad_obj)  # type: ignore


def test_from_dict_negative_invalid_data():
    """Проверка выброса исключения при несовпадении структуры словаря и целевого класса"""

    with pytest.raises(EventMapperException):
        EventMapper.from_dict({"wrong_field": 1}, SimpleEvent)
