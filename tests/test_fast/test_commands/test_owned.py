from aiogram import Router
from hamcrest import assert_that, contains_string, has_length, instance_of

from src.commands.friend import FriendCommand
from src.commands.owned import OwnedCommand
from tests.test_fast.fakes import FakeFriends, FakeHandler, FakeMessage, FakeUser


async def test_passes_owner_message_to_origin():
    handler = FakeHandler()
    await OwnedCommand(FriendCommand(FakeFriends([])), 3020).guard(
        handler, FakeMessage("/f @dawn_crane", FakeUser(3020)), {}
    )
    assert_that(
        handler.events,
        has_length(1),
        "The owned command must pass the owner message to the origin handler",
    )


async def test_refuses_stranger_politely():
    message = FakeMessage("/fl", FakeUser(404404))
    await OwnedCommand(FriendCommand(FakeFriends([])), 111).guard(
        FakeHandler(), message, {}
    )
    assert_that(
        message.replies[0],
        contains_string("owner"),
        "The owned command must refuse a stranger with a polite owner-only note",
    )


async def test_keeps_stranger_message_away_from_origin():
    handler = FakeHandler()
    await OwnedCommand(FriendCommand(FakeFriends([])), 808).guard(
        handler, FakeMessage("/f @gray_stork", FakeUser(23901)), {}
    )
    assert_that(
        handler.events,
        has_length(0),
        "The owned command must keep a stranger message away from the origin",
    )


def test_builds_aiogram_router():
    assert_that(
        OwnedCommand(FriendCommand(FakeFriends([])), 5).router(),
        instance_of(Router),
        "The owned command must build an aiogram router",
    )
