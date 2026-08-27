from aiogram import Router
from hamcrest import assert_that, contains_string, instance_of

from src.commands.start import StartCommand
from tests.test_fast.fakes import FakeMessage


async def test_answers_greeting_with_bot_name():
    message = FakeMessage()
    await StartCommand("Pixel Falcon").answer(message)
    assert_that(
        message.replies[0],
        contains_string("Pixel Falcon"),
        "The start command must answer with a greeting that shows the bot name",
    )


def test_builds_aiogram_router():
    assert_that(
        StartCommand("Echo-7").router(),
        instance_of(Router),
        "The start command must build an aiogram router",
    )
