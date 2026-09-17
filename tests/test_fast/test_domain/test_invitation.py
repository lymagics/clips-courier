from hamcrest import assert_that, ends_with, starts_with

from src.domain.invitation import Invitation


def test_points_to_bot_start_command():
    assert_that(
        Invitation("north_courier_bot", "k9-Xz_q").text(),
        starts_with("https://t.me/north_courier_bot?start="),
        "The invitation must point to the start command of the bot",
    )


def test_carries_token_as_payload():
    assert_that(
        Invitation("dusk_bot", "Zq_7-aB").text(),
        ends_with("Zq_7-aB"),
        "The invitation must carry the token as the start payload",
    )
