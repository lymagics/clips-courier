import shutil
from pathlib import Path

from hamcrest import assert_that, has_item, has_length

from src.sqlite.friends import SqliteFriends


async def test_lists_added_friend():
    folder = Path("tmp/test-friends-add")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    friends = SqliteFriends(folder / "friends.db")
    await friends.add("amber_lynx")
    assert_that(
        [friend.name() for friend in await friends.roster()],
        has_item("amber_lynx"),
        "The sqlite friends must list an added friend",
    )


async def test_keeps_single_record_for_repeated_add():
    folder = Path("tmp/test-friends-twice")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    friends = SqliteFriends(folder / "friends.db")
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
    friends = SqliteFriends(folder / "friends.db")
    await friends.add("brave_toad")
    await friends.remove("brave_toad")
    assert_that(
        await friends.roster(),
        has_length(0),
        "The sqlite friends must forget a removed friend",
    )


async def test_builds_empty_roster_from_fresh_database():
    folder = Path("tmp/test-friends-fresh")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    assert_that(
        await SqliteFriends(folder / "friends.db").roster(),
        has_length(0),
        "The sqlite friends must build an empty roster from a fresh database",
    )
