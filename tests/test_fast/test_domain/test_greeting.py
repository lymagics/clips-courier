from hamcrest import assert_that, contains_string

from src.domain.greeting import Greeting


def test_shows_configured_bot_name():
    assert_that(
        Greeting("Quirky Squirrel 3000").text(),
        contains_string("Quirky Squirrel 3000"),
        "The greeting must show the configured bot name",
    )


def test_falls_back_to_neutral_name_when_blank():
    assert_that(
        Greeting("").text(),
        contains_string("Clips Courier"),
        "The greeting must fall back to a neutral name when none is set",
    )


def test_points_newcomer_to_help_command():
    assert_that(
        Greeting("Zippy").text(),
        contains_string("/h"),
        "The greeting must point the newcomer to the help command",
    )
