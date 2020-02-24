import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from postgresql_event_store import PostgreSQLEventStore, ConcurrentStreamWriteError
from order_aggregate import Order
from model import init_db

pg_host = os.environ.get("PGHOST")
pg_database = os.environ.get("PGDATABASE")
pg_user = os.environ.get("PGUSER")
pg_password = os.environ.get("PGPASSWORD")

engine = create_engine(f"postgresql://{pg_user}:{pg_password}@{pg_host}/{pg_database}")
init_db(engine)

Session = sessionmaker(bind=engine, autocommit=True)
session = Session()

event_store = PostgreSQLEventStore(session)

# order = Order.create(1)
# order.set_status("new")
# order.set_status("paid")
# order.set_status("confirmed")
# order.set_status("shipped")
# try:
#     event_store.append_to_stream(order.uuid, order.changes)
# except ConcurrentStreamWriteError:
#     raise Exception("Can't write")

aggregate_uuid = uuid.UUID("483b8c13-dd96-4611-ae9e-940234feccd1")
event_stream = event_store.load_stream(aggregate_uuid)
order = Order(event_stream)

print(order.__dict__)
