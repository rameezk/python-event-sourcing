from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship

Base = declarative_base()


def init_db(engine):
    Base.metadata.create_all(engine)


class AggregateModel(Base):
    __tablename__ = "aggregates"

    uuid = Column("uuid", String(length=36), nullable=False, primary_key=True)
    version = Column("version", Integer, nullable=False, default=1)


class EventModel(Base):
    __tablename__ = "events"

    uuid = Column("uuid", String(length=36), nullable=False, primary_key=True)
    aggregate_uuid = Column(
        "aggregate_uuid",
        String(length=36),
        ForeignKey("aggregates.uuid"),
        nullable=False,
    )
    name = Column("name", String(length=50), nullable=False)
    data = Column("data", JSON)

    aggregate = relationship(AggregateModel, uselist=False, backref="events")
