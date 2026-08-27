from aiogram import Router
from hamcrest import assert_that, contains_string, instance_of, not_

from src.commands.help import HelpCommand
from tests.test_fast.fakes import FakeMessage, FakeUser


async def test_answers_manual_with_start_command():
    message = FakeMessage("/h", FakeUser(7501))
    await HelpCommand("Comet", 42007).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/s"),
        "The help command must answer with a manual that lists the start command",
    )


async def test_shows_owner_commands_to_owner():
    message = FakeMessage("/h", FakeUser(6100))
    await HelpCommand("Orbit", 6100).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/fl"),
        "The help command must show the owner commands to the owner",
    )


async def test_hides_owner_commands_from_friend():
    message = FakeMessage("/h", FakeUser(2288))
    await HelpCommand("Lumen", 990022).answer(message)
    assert_that(
        message.replies[0],
        not_(contains_string("/fl")),
        "The help command must hide the owner commands from a friend",
    )


def test_builds_aiogram_router():
    assert_that(
        HelpCommand("Nebula", 314).router(),
        instance_of(Router),
        "The help command must build an aiogram router",
    )
