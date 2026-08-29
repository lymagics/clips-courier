import asyncio
from os import environ

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import Connection, pool
from sqlalchemy.ext.asyncio import async_engine_from_config

load_dotenv()

config = context.config
if not config.get_main_option("sqlalchemy.url"):
    config.set_main_option(
        "sqlalchemy.url",
        "sqlite+aiosqlite:///" + environ.get("DB_PATH", "courier.db"),
    )


def migrate(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=None)
    with context.begin_transaction():
        context.run_migrations()


async def upgrade() -> None:
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with engine.connect() as connection:
        await connection.run_sync(migrate)
    await engine.dispose()


asyncio.run(upgrade())
