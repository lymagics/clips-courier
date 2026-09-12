import asyncio
import shutil
from pathlib import Path

from hamcrest import assert_that, has_item, has_length
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from src.sqlite.friends import SqliteFriends
from tests.test_fast.schema import MigratedSchema


async def test_lists_added_friend():
    folder = Path("tmp/test-friends-add")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "courier.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/courier.db", poolclass=NullPool
    )
    friends = SqliteFriends(engine)
    await friends.add("amber_lynx")
    assert_that(
        [friend.name() for friend in await friends.roster()],
        has_item("amber_lynx"),
        "The sqlite friends must list an added friend",
    )


async def test_keeps_single_record_for_repeated_add():
    folder = Path("tmp/test-friends-repeat")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "twice.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/twice.db", poolclass=NullPool
    )
    friends = SqliteFriends(engine)
    await friends.add("iron_sparrow")
    await friends.add("iron_sparrow")
    assert_that(
        await friends.roster(),
        has_length(1),
        "The sqlite friends must keep a single record for a repeated add",
    )


async def test_forgets_removed_friend():
    folder = Path("tmp/test-friends-remove")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "gone.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/gone.db", poolclass=NullPool
    )
    friends = SqliteFriends(engine)
    await friends.add("brave_toad")
    await friends.remove("brave_toad")
    assert_that(
        await friends.roster(),
        has_length(0),
        "The sqlite friends must forget a removed friend",
    )


async def test_builds_empty_roster_from_fresh_database():
    folder = Path("tmp/test-friends-empty")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "blank.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/blank.db", poolclass=NullPool
    )
    assert_that(
        await SqliteFriends(engine).roster(),
        has_length(0),
        "The sqlite friends must build an empty roster from a fresh database",
    )


async def test_adds_friends_from_concurrent_tasks():
    folder = Path("tmp/test-friends-concurrent")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "race.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/race.db", poolclass=NullPool
    )
    friends = SqliteFriends(engine)
    await asyncio.gather(
        friends.add("quick_ibis"),
        friends.add("quiet_yak"),
        friends.add("quirky_eel"),
        friends.add("queasy_gnu"),
    )
    assert_that(
        await friends.roster(),
        has_length(4),
        "The sqlite friends must add friends from concurrent tasks",
    )
