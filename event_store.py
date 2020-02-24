import abc
import uuid
import typing
from dataclasses import dataclass, asdict


@dataclass
class Event:
    def as_dict(self):
        thing = asdict(self)
        return thing


class EventStream:
    events: typing.List[Event]
    version: int

    def __init__(self, events: typing.List[Event], version: int = 1):
        self.events = events
        self.version = version


class EventStore(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def load_stream(self, aggregate_uuid: uuid.UUID) -> EventStream:
        pass

    @abc.abstractmethod
    def append_to_stream(
        self,
        aggregate_uuid: uuid.UUID,
        expected_version: typing.Optional[int],
        events: typing.List[Event],
    ) -> None:
        pass


class ConcurrentStreamWriteError(RuntimeError):
    pass
