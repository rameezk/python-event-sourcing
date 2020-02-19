import functools
from dataclasses import dataclass


def method_dispatch(func):
    dispatcher = functools.singledispatch(func)

    def wrapper(*args, **kwargs):
        return dispatcher.dispatch(args[1].__class__)(*args, **kwargs)

    wrapper.register = dispatcher.register
    functools.update_wrapper(wrapper, func)
    return wrapper


@dataclass
class OrderCreated:
    user_id: int


@dataclass
class StatusChanged:
    new_status: str


class Order:
    def __init__(self, events: list):
        self.user_id = None
        self.status = None

        for event in events:
            self.apply(event)

        self.changes = []

    @method_dispatch
    def apply(self, event):
        raise ValueError("Unknown event!")

    @apply.register(OrderCreated)
    def _(self, event: OrderCreated):
        self.user_id = event.user_id
        self.status = "new"

    @apply.register(StatusChanged)
    def _(self, event: StatusChanged):
        self.status = event.new_status

    def set_status(self, new_status: str):
        if new_status not in ("new", "paid", "confirmed", "shipped"):
            raise ValueError(f"{new_status} is not a correct status!")

        event = StatusChanged(new_status)
        self.apply(event)
        self.changes.append(event)

    @classmethod
    def create(cls, user_id: int):
        initial_event = OrderCreated(user_id)
        instance = cls([initial_event])
        instance.changes = [initial_event]
        return instance
