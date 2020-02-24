from sqlalchemy import (
    Table,
    MetaData,
    Column,
    String,
    Integer,
    ForeignKey,
    JSON,
    Index,
    create_engine,
)
import os

metadata = MetaData()
aggregates = Table(
    "aggregates",
    metadata,
    Column("uuid", String(length=36), nullable=False, primary_key=True),
    Column("version", Integer, default=1, nullable=False),
)

events = Table(
    "events",
    metadata,
    Column("uuid", String(length=36), nullable=False, primary_key=True),
    Column(
        "aggregate_uuid",
        String(length=36),
        ForeignKey("aggregates.uuid"),
        nullable=False,
    ),
    Column("name", String(length=50), nullable=False),
    Column("data", JSON),
)

Index("aggregate_uuid_idx", events.columns.aggregate_uuid)

pg_host = os.environ.get("PGHOST")
pg_database = os.environ.get("PGDATABASE")
pg_user = os.environ.get("PGUSER")
pg_password = os.environ.get("PGPASSWORD")

engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}")

metadata.create_all(engine)
