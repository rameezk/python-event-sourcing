import typing
import uuid
import json
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.orm.exc import NoResultFound

from event_store import Event, EventStream, EventStore, ConcurrentStreamWriteError
from model import AggregateModel, EventModel
import events


class NotFound(object):
    pass


class PostgreSQLEventStore(EventStore):
    def __init__(self, session: Session):
        self.session = session

    def load_stream(self, aggregate_uuid: uuid.UUID) -> EventStream:
        try:
            aggregate: AggregateModel = self.session.query(AggregateModel).options(
                joinedload("events")
            ).filter(AggregateModel.uuid == str(aggregate_uuid)).one()

        except NoResultFound:
            raise NotFound

        event_objects = [self._translate_to_object(model) for model in aggregate.events]
        version = aggregate.version

        return EventStream(event_objects, version)

    def _translate_to_object(self, event_model: EventModel) -> Event:
        class_name = event_model.name
        kwargs = event_model.data
        event_class: typing.Type[Event] = getattr(events, class_name)
        return event_class(**kwargs)

    def append_to_stream(
        self,
        aggregate_uuid: uuid.UUID,
        events: typing.List[Event],
        expected_version: typing.Optional[int] = None,
    ) -> None:
        connection = self.session.connection()

        if expected_version:  # update
            stmt = (
                AggregateModel.__table_name__.update()
                .values(version=expected_version + 1)
                .where(
                    (AggregateModel.version == expected_version)
                    & (AggregateModel.uuid == str(aggregate_uuid))
                )
            )
            result_proxy = connection.execute(stmt)

            if result_proxy.rowcount != 1:
                raise ConcurrentStreamWriteError
        else:  # new aggregate
            stmt = AggregateModel.__table__.insert().values(
                uuid=str(aggregate_uuid), version=1
            )
            connection.execute(stmt)

            for event in events:
                aggregate_uuid_str = str(aggregate_uuid)
                event_as_dict = event.as_dict()

                connection.execute(
                    EventModel.__table__.insert().values(
                        uuid=str(uuid.uuid4()),
                        aggregate_uuid=aggregate_uuid_str,
                        name=event.__class__.__name__,
                        data=event_as_dict,
                    )
                )

                payload = json.dumps(event_as_dict)
                connection.execute(
                    f"NOTIFY events, '{aggregate_uuid_str}_{event.__class__.__name__}_{payload}'"
                )
