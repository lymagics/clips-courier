from aiogram import Router
from hamcrest import assert_that, contains_string, has_length, instance_of

from src.commands.start import StartCommand
from src.commands.trusted import TrustedCommand
from tests.test_fast.fakes import FakeFriends, FakeHandler, FakeMessage, FakeUser


async def test_passes_owner_message_to_origin():
    handler = FakeHandler()
    await TrustedCommand(StartCommand("Argo"), 5108, FakeFriends({})).guard(
        handler, FakeMessage("/d https://example.test/v/17", FakeUser(5108)), {}
    )
    assert_that(
        handler.events,
        has_length(1),
        "The trusted command must pass the owner message to the origin handler",
    )


async def test_passes_friend_message_to_origin():
    handler = FakeHandler()
    await TrustedCommand(
        StartCommand("Vega"), 62003, FakeFriends({88190: "copper_owl"})
    ).guard(
        handler,
        FakeMessage("/d https://example.test/v/240", FakeUser(88190, "copper_owl")),
        {},
    )
    assert_that(
        handler.events,
        has_length(1),
        "The trusted command must pass a friend message to the origin handler",
    )


async def test_keeps_renamed_friend_trusted():
    handler = FakeHandler()
    await TrustedCommand(
        StartCommand("Rhea"), 41225, FakeFriends({75301: "silk_moth77"})
    ).guard(
        handler,
        FakeMessage("/d https://example.test/v/33", FakeUser(75301, "velvet_moth")),
        {},
    )
    assert_that(
        handler.events,
        has_length(1),
        "The trusted command must keep a friend trusted after a username change",
    )


async def test_refuses_stranger_holding_friend_old_username():
    handler = FakeHandler()
    await TrustedCommand(
        StartCommand("Lyra"), 253, FakeFriends({12: "dune_hare"})
    ).guard(
        handler,
        FakeMessage("/d https://example.test/v/812", FakeUser(909111, "dune_hare")),
        {},
    )
    assert_that(
        handler.events,
        has_length(0),
        "The trusted command must refuse a stranger who took a friend's username",
    )


async def test_refuses_stranger_with_denial():
    message = FakeMessage(
        "/d https://example.test/v/512", FakeUser(707111, "sly_gnat9")
    )
    await TrustedCommand(
        StartCommand("Ceres"), 380, FakeFriends({4: "tidal_wolf"})
    ).guard(FakeHandler(), message, {})
    assert_that(
        message.replies[0],
        contains_string("denied"),
        "The trusted command must refuse a stranger with an access denied note",
    )


async def test_keeps_stranger_message_away_from_origin():
    handler = FakeHandler()
    await TrustedCommand(StartCommand("Juno"), 381, FakeFriends({})).guard(
        handler, FakeMessage("/d https://example.test/v/6", FakeUser(72646)), {}
    )
    assert_that(
        handler.events,
        has_length(0),
        "The trusted command must keep a stranger message away from the origin",
    )


def test_builds_aiogram_router():
    assert_that(
        TrustedCommand(StartCommand("Nautilus"), 12, FakeFriends({})).router(),
        instance_of(Router),
        "The trusted command must build an aiogram router",
    )
