from aiogram import Router
from hamcrest import assert_that, contains_string, has_item, instance_of, not_

from src.commands.removal import RemovalCommand
from tests.test_fast.fakes import FakeFriends, FakeMessage


async def test_removes_friend_from_list():
    friends = FakeFriends(["stone_finch"])
    await RemovalCommand(friends).answer(FakeMessage("/kf @stone_finch"))
    assert_that(
        friends.names,
        not_(has_item("stone_finch")),
        "The removal command must remove the given username from the list",
    )


async def test_confirms_removal():
    message = FakeMessage("/kf @pale_viper")
    await RemovalCommand(FakeFriends(["pale_viper"])).answer(message)
    assert_that(
        message.replies[0],
        contains_string("pale_viper"),
        "The removal command must confirm the removal with the username",
    )


async def test_shows_usage_when_username_missing():
    message = FakeMessage("/kf")
    await RemovalCommand(FakeFriends([])).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/kf @username"),
        "The removal command must show its usage when no username is given",
    )


def test_builds_aiogram_router():
    assert_that(
        RemovalCommand(FakeFriends([])).router(),
        instance_of(Router),
        "The removal command must build an aiogram router",
    )
