from hamcrest import assert_that, equal_to, is_

from src.domain.utf16 import Utf16Text


def test_counts_astral_emoji_as_two_units():
    assert_that(
        Utf16Text("🚀🪐").units(),
        is_(4),
        "The utf-16 text must count each astral-plane emoji as two code units",
    )


def test_counts_plain_letters_as_one_unit_each():
    assert_that(
        Utf16Text("orbit").units(),
        is_(5),
        "The utf-16 text must count each plain letter as one code unit",
    )


def test_keeps_short_text_whole_when_room_is_ample():
    assert_that(
        Utf16Text("tiny 🐝 bee").clipped(64),
        equal_to("tiny 🐝 bee"),
        "The utf-16 text must keep a short text whole when the room is ample",
    )


def test_drops_emoji_that_does_not_fit_in_remaining_unit():
    assert_that(
        Utf16Text("hi🎉").clipped(3),
        equal_to("hi"),
        "The utf-16 text must drop an emoji that does not fit whole "
        "into the last remaining code unit instead of splitting its surrogate pair",
    )


def test_cuts_text_to_exact_room_in_units():
    assert_that(
        Utf16Text("🍉melon").clipped(4),
        equal_to("🍉me"),
        "The utf-16 text must cut the text to exactly the given room in code units",
    )


def test_clips_to_nothing_for_negative_room():
    assert_that(
        Utf16Text("vanish").clipped(-7),
        equal_to(""),
        "The utf-16 text must clip to nothing when the room is negative",
    )
