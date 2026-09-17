from aiogram import Router
from hamcrest import assert_that, contains_string, ends_with, instance_of

from src.commands.friends import FriendsCommand
from tests.test_fast.fakes import FakeFriends, FakeMessage


async def test_lists_friend_usernames():
    message = FakeMessage("/fl")
    await FriendsCommand(FakeFriends({4401: "mellow_crow", 4402: "tidal_wolf"})).answer(
        message
    )
    assert_that(
        message.replies[0],
        contains_string("@tidal_wolf"),
        "The friends command must list the username of every friend",
    )


async def test_lists_friend_ids():
    message = FakeMessage("/fl")
    await FriendsCommand(FakeFriends({70301: "amber_newt"})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("70301"),
        "The friends command must list the telegram id of every friend",
    )


async def test_lists_id_alone_for_nameless_friend():
    message = FakeMessage("/fl")
    await FriendsCommand(FakeFriends({99120: ""})).answer(message)
    assert_that(
        message.replies[0],
        ends_with("\n99120"),
        "The friends command must list the id alone for a nameless friend",
    )


async def test_reports_empty_list():
    message = FakeMessage("/fl")
    await FriendsCommand(FakeFriends({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("no friends"),
        "The friends command must report when the list is empty",
    )


def test_builds_aiogram_router():
    assert_that(
        FriendsCommand(FakeFriends({})).router(),
        instance_of(Router),
        "The friends command must build an aiogram router",
    )
