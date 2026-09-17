from aiogram import Router
from hamcrest import assert_that, contains_string, has_key, instance_of, not_

from src.commands.removal import RemovalCommand
from tests.test_fast.fakes import FakeFriends, FakeMessage


async def test_removes_friend_by_id():
    friends = FakeFriends({31001: "stone_finch"})
    await RemovalCommand(friends).answer(FakeMessage("/kf 31001"))
    assert_that(
        friends.members,
        not_(has_key(31001)),
        "The removal command must remove the friend with the given id",
    )


async def test_removes_friend_by_username():
    friends = FakeFriends({4477: "pale_viper"})
    await RemovalCommand(friends).answer(FakeMessage("/kf @pale_viper"))
    assert_that(
        friends.members,
        not_(has_key(4477)),
        "The removal command must remove the friend with the given username",
    )


async def test_matches_username_regardless_of_case():
    friends = FakeFriends({8811: "moss_kestrel"})
    await RemovalCommand(friends).answer(FakeMessage("/kf @Moss_Kestrel"))
    assert_that(
        friends.members,
        not_(has_key(8811)),
        "The removal command must match a username regardless of case",
    )


async def test_confirms_removal():
    message = FakeMessage("/kf @dune_hare")
    await RemovalCommand(FakeFriends({5: "dune_hare"})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("dune_hare"),
        "The removal command must confirm the removal with the username",
    )


async def test_points_to_list_for_unknown_friend():
    message = FakeMessage("/kf @ghost_tern")
    await RemovalCommand(FakeFriends({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/fl"),
        "The removal command must point to the friend list for an unknown friend",
    )


async def test_shows_usage_when_target_missing():
    message = FakeMessage("/kf")
    await RemovalCommand(FakeFriends({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/kf @username"),
        "The removal command must show its usage when no target is given",
    )


async def test_shows_usage_for_malformed_target():
    message = FakeMessage("/kf uncle bob")
    await RemovalCommand(FakeFriends({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/kf @username"),
        "The removal command must show its usage for a malformed target",
    )


def test_builds_aiogram_router():
    assert_that(
        RemovalCommand(FakeFriends({})).router(),
        instance_of(Router),
        "The removal command must build an aiogram router",
    )
