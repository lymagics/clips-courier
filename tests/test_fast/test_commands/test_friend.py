import time

from aiogram import Router
from hamcrest import (
    assert_that,
    contains_string,
    ends_with,
    greater_than,
    has_length,
    instance_of,
)

from src.commands.friend import FriendCommand
from tests.test_fast.fakes import FakeBot, FakeInvites, FakeMessage


async def test_answers_with_deep_link_to_bot():
    message = FakeMessage("/f", bot=FakeBot("north_courier_bot"))
    await FriendCommand(FakeInvites({}), 24).answer(message)
    assert_that(
        message.replies[0],
        contains_string("https://t.me/north_courier_bot?start="),
        "The friend command must answer with a deep link to the bot",
    )


async def test_stores_minted_token():
    invites = FakeInvites({})
    await FriendCommand(invites, 12).answer(FakeMessage("/f"))
    assert_that(
        invites.deadlines,
        has_length(1),
        "The friend command must store the minted token",
    )


async def test_puts_stored_token_into_link():
    invites = FakeInvites({})
    message = FakeMessage("/f", bot=FakeBot("west_courier_bot"))
    await FriendCommand(invites, 3).answer(message)
    assert_that(
        message.replies[0],
        ends_with(next(iter(invites.deadlines))),
        "The friend command must put the stored token into the link",
    )


async def test_sets_deadline_ahead_of_now():
    invites = FakeInvites({})
    await FriendCommand(invites, 1).answer(FakeMessage("/f"))
    assert_that(
        next(iter(invites.deadlines.values())),
        greater_than(int(time.time())),
        "The friend command must set the token deadline ahead of now",
    )


async def test_mentions_expiry_in_hours():
    message = FakeMessage("/f")
    await FriendCommand(FakeInvites({}), 6).answer(message)
    assert_that(
        message.replies[0],
        contains_string("6 hours"),
        "The friend command must mention the link expiry in hours",
    )


def test_builds_aiogram_router():
    assert_that(
        FriendCommand(FakeInvites({}), 24).router(),
        instance_of(Router),
        "The friend command must build an aiogram router",
    )
