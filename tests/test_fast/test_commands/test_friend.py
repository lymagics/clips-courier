from aiogram import Router
from hamcrest import assert_that, contains_string, has_item, instance_of

from src.commands.friend import FriendCommand
from tests.test_fast.fakes import FakeFriends, FakeMessage


async def test_adds_friend_to_list():
    friends = FakeFriends([])
    await FriendCommand(friends).answer(FakeMessage("/f @night_fox9"))
    assert_that(
        friends.names,
        has_item("night_fox9"),
        "The friend command must add the given username to the list",
    )


async def test_lowercases_added_username():
    friends = FakeFriends([])
    await FriendCommand(friends).answer(FakeMessage("/f @LoudBadger"))
    assert_that(
        friends.names,
        has_item("loudbadger"),
        "The friend command must lowercase the added username",
    )


async def test_confirms_addition():
    message = FakeMessage("/f @glass_heron")
    await FriendCommand(FakeFriends([])).answer(message)
    assert_that(
        message.replies[0],
        contains_string("glass_heron"),
        "The friend command must confirm the addition with the username",
    )


async def test_shows_usage_when_username_missing():
    message = FakeMessage("/f")
    await FriendCommand(FakeFriends([])).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/f @username"),
        "The friend command must show its usage when no username is given",
    )


async def test_shows_usage_for_malformed_username():
    message = FakeMessage("/f uncle bob")
    await FriendCommand(FakeFriends([])).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/f @username"),
        "The friend command must show its usage for a malformed username",
    )


def test_builds_aiogram_router():
    assert_that(
        FriendCommand(FakeFriends([])).router(),
        instance_of(Router),
        "The friend command must build an aiogram router",
    )
