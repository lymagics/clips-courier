from hamcrest import assert_that, has_length

from src.bot import Bot
from src.commands.help import HelpCommand
from src.commands.start import StartCommand


def test_builds_dispatcher_with_router_per_command():
    assert_that(
        Bot(
            StartCommand("Kestrel"),
            HelpCommand("Kestrel", 777001),
        )
        .bot("42:TEST-token")
        .sub_routers,
        has_length(2),
        "The bot must include one router per given command",
    )
