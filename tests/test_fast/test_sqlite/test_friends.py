from hamcrest import assert_that, has_item, has_length

from src.sqlite.friends import SqliteFriends
from tests.test_fast.fakes import FakeSession


async def test_lists_added_friend():
    friends = SqliteFriends(FakeSession())
    await friends.add("amber_lynx")
    assert_that(
        [friend.name() for friend in await friends.roster()],
        has_item("amber_lynx"),
        "The sqlite friends must list an added friend",
    )


async def test_keeps_single_record_for_repeated_add():
    friends = SqliteFriends(FakeSession())
    await friends.add("iron_sparrow")
    await friends.add("iron_sparrow")
    assert_that(
        await friends.roster(),
        has_length(1),
        "The sqlite friends must keep a single record for a repeated add",
    )


async def test_forgets_removed_friend():
    friends = SqliteFriends(FakeSession())
    await friends.add("brave_toad")
    await friends.remove("brave_toad")
    assert_that(
        await friends.roster(),
        has_length(0),
        "The sqlite friends must forget a removed friend",
    )


async def test_builds_empty_roster_from_untouched_session():
    assert_that(
        await SqliteFriends(FakeSession()).roster(),
        has_length(0),
        "The sqlite friends must build an empty roster from an untouched session",
    )
