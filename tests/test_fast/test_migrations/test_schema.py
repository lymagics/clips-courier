import shutil
import sqlite3
from pathlib import Path

from hamcrest import assert_that, has_item, has_length
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.sqlite.friends import SqliteFriends
from tests.test_fast.schema import MigratedSchema


async def test_builds_friends_table_in_fresh_database():
    folder = Path("tmp/test-schema-fresh")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "courier.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/courier.db", poolclass=NullPool
    )
    assert_that(
        await SqliteFriends(AsyncSession(engine)).roster(),
        has_length(0),
        "The migrated schema must build a friends table in a fresh database",
    )


async def test_survives_repeated_upgrade():
    folder = Path("tmp/test-schema-repeat")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    schema = MigratedSchema(folder / "wire.db")
    await schema.upgrade()
    await schema.upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/wire.db", poolclass=NullPool
    )
    friends = SqliteFriends(AsyncSession(engine))
    await friends.add("velvet_owl")
    assert_that(
        [friend.name() for friend in await friends.roster()],
        has_item("velvet_owl"),
        "The migrated schema must survive a repeated upgrade",
    )


async def test_adopts_database_born_before_migrations():
    folder = Path("tmp/test-schema-legacy")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    legacy = sqlite3.connect(folder / "legacy.db")
    legacy.execute("CREATE TABLE friends (name TEXT PRIMARY KEY)")
    legacy.execute("INSERT INTO friends (name) VALUES ('rusty_finch')")
    legacy.commit()
    legacy.close()
    await MigratedSchema(folder / "legacy.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/legacy.db", poolclass=NullPool
    )
    assert_that(
        [
            friend.name()
            for friend in await SqliteFriends(AsyncSession(engine)).roster()
        ],
        has_item("rusty_finch"),
        "The migrated schema must adopt a database born before migrations",
    )
