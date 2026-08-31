from hamcrest import assert_that, ends_with, equal_to, is_

from src.domain.caption import Caption


def test_joins_description_and_attribution_footer():
    assert_that(
        Caption("Cat jumps over a very lazy dog 🐈", "whisker_flix", "TikTok").text(),
        equal_to("Cat jumps over a very lazy dog 🐈\n\n— @whisker_flix · TikTok"),
        "The caption must join the description and the attribution footer",
    )


def test_shrinks_long_description_to_telegram_limit():
    assert_that(
        len(Caption("z" * 4097, "marathon_talker", "Instagram").text()),
        is_(1024),
        "The caption must shrink a long description to the telegram limit",
    )


def test_keeps_footer_intact_after_shrinking():
    assert_that(
        Caption("y" * 2049, "night_owl_9", "X").text(),
        ends_with("— @night_owl_9 · X"),
        "The caption must keep the footer intact after shrinking",
    )


def test_shows_footer_alone_without_description():
    assert_that(
        Caption("", "quiet_lynx", "X").text(),
        equal_to("— @quiet_lynx · X"),
        "The caption must show the footer alone without a description",
    )


def test_drops_handle_for_nameless_account():
    assert_that(
        Caption("Sunset timelapse over the bay", "", "Instagram").text(),
        equal_to("Sunset timelapse over the bay\n\n— Instagram"),
        "The caption must drop the handle for a nameless account",
    )


def test_keeps_single_at_sign_for_prefixed_account():
    assert_that(
        Caption("Bloopers #7", "@double_at", "TikTok").text(),
        equal_to("Bloopers #7\n\n— @double_at · TikTok"),
        "The caption must keep a single at sign for a prefixed account",
    )


def test_trims_whitespace_around_description():
    assert_that(
        Caption(" \n\t padded premiere \t\n ", "tidy_beaver", "X").text(),
        equal_to("padded premiere\n\n— @tidy_beaver · X"),
        "The caption must trim the whitespace around the description",
    )
