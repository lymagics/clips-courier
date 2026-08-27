import pytest
from hamcrest import assert_that, equal_to, is_

from src.domain.handle import Handle


def test_strips_at_sign_and_lowercases():
    assert_that(
        Handle("@NightFox_88").name(),
        equal_to("nightfox_88"),
        "The handle must strip the at-sign and lowercase the username",
    )


def test_valid_for_plain_username():
    assert_that(
        Handle("cosmic_otter").valid(),
        is_(True),
        "The handle must be valid for a plain username without an at-sign",
    )


@pytest.mark.parametrize("text", ["@ab", "two words", "dash-name", ""])
def test_invalid_for_malformed_text(text: str):
    assert_that(
        Handle(text).valid(),
        is_(False),
        f"The handle must be invalid for the malformed text {text!r}",
    )
