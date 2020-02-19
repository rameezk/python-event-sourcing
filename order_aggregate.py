from dataclasses import dataclass

# How one would typically model an e-commerce order
#
# class Order:
#     def __init__(self, user_id: int, status: str = "new"):
#         self.user_id = user_id
#         self.status = status
#
#     def set_status(self, new_status: str):
#         if new_status not in ("new", "paid", "confirmed", "shipped"):
#             raise ValueError(f"{new_status} is not a correct status!")
#
#         self.status = new_status
#

# But what "events" will mutate the state?
# -- if a status changes
# -- if a user_id changes (new order is created?)


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

    def apply(self, event):
        if isinstance(event, OrderCreated):
            event: OrderCreated = event
            self.user_id = event.user_id
            self.status = "new"
        elif isinstance(event, StatusChanged):
            event: StatusChanged = event
            self.status = event.new_status
        else:
            raise ValueError("Unknown event!")

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
