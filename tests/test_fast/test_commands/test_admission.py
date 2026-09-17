from aiogram import Router
from hamcrest import (
    assert_that,
    contains_string,
    has_entry,
    has_key,
    has_length,
    has_value,
    instance_of,
    not_,
)

from src.commands.admission import AdmissionCommand
from tests.test_fast.fakes import FakeFriends, FakeInvites, FakeMessage, FakeUser


async def test_admits_link_bearer_by_id():
    friends = FakeFriends({})
    await AdmissionCommand(FakeInvites({"Qw3rTy-u": 4102444800}), friends).answer(
        FakeMessage("/start Qw3rTy-u", FakeUser(55123, "misty_kite"))
    )
    assert_that(
        friends.members,
        has_key(55123),
        "The admission command must admit the link bearer by telegram id",
    )


async def test_records_bearer_username():
    friends = FakeFriends({})
    await AdmissionCommand(FakeInvites({"a1B2c3": 4102444800}), friends).answer(
        FakeMessage("/start a1B2c3", FakeUser(60771, "cedar_lark"))
    )
    assert_that(
        friends.members,
        has_entry(60771, "cedar_lark"),
        "The admission command must record the username of the bearer",
    )


async def test_lowercases_bearer_username():
    friends = FakeFriends({})
    await AdmissionCommand(FakeInvites({"zz_Top9": 4102444800}), friends).answer(
        FakeMessage("/start zz_Top9", FakeUser(48002, "LoudBadger"))
    )
    assert_that(
        friends.members,
        has_value("loudbadger"),
        "The admission command must lowercase the username of the bearer",
    )


async def test_records_blank_name_for_bearer_without_username():
    friends = FakeFriends({})
    await AdmissionCommand(FakeInvites({"noname-7": 4102444800}), friends).answer(
        FakeMessage("/start noname-7", FakeUser(73))
    )
    assert_that(
        friends.members,
        has_value(""),
        "The admission command must record a blank name for a nameless bearer",
    )


async def test_spends_token_on_admission():
    invites = FakeInvites({"once_only": 4102444800})
    await AdmissionCommand(invites, FakeFriends({})).answer(
        FakeMessage("/start once_only", FakeUser(91, "pine_wren"))
    )
    assert_that(
        invites.deadlines,
        not_(has_key("once_only")),
        "The admission command must spend the token on admission",
    )


async def test_welcomes_admitted_bearer():
    message = FakeMessage("/start hello-42", FakeUser(2048, "opal_hare"))
    await AdmissionCommand(
        FakeInvites({"hello-42": 4102444800}), FakeFriends({})
    ).answer(message)
    assert_that(
        message.replies[0],
        contains_string("Welcome"),
        "The admission command must welcome the admitted bearer",
    )


async def test_refuses_expired_link():
    friends = FakeFriends({})
    await AdmissionCommand(FakeInvites({"stale_1": 946684800}), friends).answer(
        FakeMessage("/start stale_1", FakeUser(3011, "late_owl"))
    )
    assert_that(
        friends.members,
        has_length(0),
        "The admission command must refuse an expired link",
    )


async def test_explains_refusal_of_unknown_token():
    message = FakeMessage("/start forged-x", FakeUser(6006, "sly_gnat"))
    await AdmissionCommand(FakeInvites({}), FakeFriends({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("expired"),
        "The admission command must explain the refusal of an unknown token",
    )


async def test_refuses_bearer_without_sender():
    friends = FakeFriends({})
    await AdmissionCommand(FakeInvites({"ghost-9": 4102444800}), friends).answer(
        FakeMessage("/start ghost-9")
    )
    assert_that(
        friends.members,
        has_length(0),
        "The admission command must refuse a message without a sender",
    )


def test_builds_aiogram_router():
    assert_that(
        AdmissionCommand(FakeInvites({}), FakeFriends({})).router(),
        instance_of(Router),
        "The admission command must build an aiogram router",
    )
