import asyncio
import aiopg
import os

pg_host = os.environ.get("PGHOST")
pg_database = os.environ.get("PGDATABASE")
pg_user = os.environ.get("PGUSER")
pg_password = os.environ.get("PGPASSWORD")

dsn = f"dbname={pg_database} user={pg_user} password={pg_password} host={pg_host}"


async def listen(conn):
    async with conn.cursor() as cur:
        await cur.execute("LISTEN events")
        while True:
            msg = await conn.notifies.get()
            print(f"Receive <- {msg.payload}")


async def main():
    async with aiopg.create_pool(dsn) as pool:
        async with pool.acquire() as conn1:
            listener = listen(conn1)
            await listener


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
