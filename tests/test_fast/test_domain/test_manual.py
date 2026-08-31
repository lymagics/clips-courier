import pytest
from hamcrest import assert_that, contains_string, not_

from src.domain.manual import Manual, OwnerManual


@pytest.mark.parametrize("command", ["/s", "/h", "/d <link>", "/dm <link>"])
def test_lists_available_command(command: str):
    assert_that(
        Manual("Vortex").text(),
        contains_string(command),
        f"The manual must list the {command} command",
    )


def test_shows_configured_bot_name():
    assert_that(
        Manual("Käpt'n Klick").text(),
        contains_string("Käpt'n Klick"),
        "The manual must show the configured bot name",
    )


def test_falls_back_to_neutral_name_when_blank():
    assert_that(
        Manual("").text(),
        contains_string("Clips Courier"),
        "The manual must fall back to a neutral name when none is set",
    )


def test_hides_owner_commands():
    assert_that(
        Manual("Zephyr-2").text(),
        not_(contains_string("/fl")),
        "The manual must hide the owner commands from a friend",
    )


@pytest.mark.parametrize("command", ["/f @username", "/fl", "/kf @username", "/st"])
def test_lists_owner_command(command: str):
    assert_that(
        OwnerManual(Manual("Quasar")).text(),
        contains_string(command),
        f"The owner manual must list the {command} command",
    )


def test_keeps_friend_commands_in_owner_view():
    assert_that(
        OwnerManual(Manual("Beacon-9")).text(),
        contains_string("/d"),
        "The owner manual must keep the friend commands in the owner view",
    )
