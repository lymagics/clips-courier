from aiogram import Router
from hamcrest import assert_that, contains_string, has_length, instance_of

from src.commands.start import StartCommand
from src.commands.trusted import TrustedCommand
from tests.test_fast.fakes import FakeFriends, FakeHandler, FakeMessage, FakeUser


async def test_passes_owner_message_to_origin():
    handler = FakeHandler()
    await TrustedCommand(StartCommand("Argo"), 5108, FakeFriends([])).guard(
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
        StartCommand("Vega"), 62003, FakeFriends(["copper_owl"])
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


async def test_matches_friend_username_regardless_of_case():
    handler = FakeHandler()
    await TrustedCommand(
        StartCommand("Rhea"), 41225, FakeFriends(["silk_moth77"])
    ).guard(
        handler,
        FakeMessage("/d https://example.test/v/33", FakeUser(75301, "Silk_Moth77")),
        {},
    )
    assert_that(
        handler.events,
        has_length(1),
        "The trusted command must match a friend username regardless of case",
    )


async def test_refuses_stranger_with_denial():
    message = FakeMessage(
        "/d https://example.test/v/812", FakeUser(909111, "sly_gnat9")
    )
    await TrustedCommand(StartCommand("Lyra"), 253, FakeFriends(["dune_hare"])).guard(
        FakeHandler(), message, {}
    )
    assert_that(
        message.replies[0],
        contains_string("denied"),
        "The trusted command must refuse a stranger with an access denied note",
    )


async def test_keeps_stranger_message_away_from_origin():
    handler = FakeHandler()
    await TrustedCommand(StartCommand("Ceres"), 380, FakeFriends([])).guard(
        handler, FakeMessage("/d https://example.test/v/6", FakeUser(72646)), {}
    )
    assert_that(
        handler.events,
        has_length(0),
        "The trusted command must keep a stranger message away from the origin",
    )


def test_builds_aiogram_router():
    assert_that(
        TrustedCommand(StartCommand("Nautilus"), 12, FakeFriends([])).router(),
        instance_of(Router),
        "The trusted command must build an aiogram router",
    )
