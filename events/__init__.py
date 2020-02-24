from dataclasses import dataclass
from event_store import Event


@dataclass
class OrderCreated(Event):
    user_id: int


@dataclass
class StatusChanged(Event):
    new_status: str
