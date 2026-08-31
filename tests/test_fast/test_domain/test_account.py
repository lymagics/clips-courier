from hamcrest import assert_that, equal_to

from src.domain.account import Account


def test_prefers_id_looking_like_handle():
    assert_that(
        Account("velvet_moth", "Velvet Moth Films").text(),
        equal_to("velvet_moth"),
        "The account must prefer an id that looks like a handle",
    )


def test_rejects_purely_numeric_id():
    assert_that(
        Account("7314159265358", "gadget_goblin").text(),
        equal_to("gadget_goblin"),
        "The account must reject a purely numeric id",
    )


def test_falls_back_to_name_for_blank_id():
    assert_that(
        Account("  ", "amber.fox.daily").text(),
        equal_to("amber.fox.daily"),
        "The account must fall back to the name for a blank id",
    )


def test_stays_empty_for_anonymous_upload():
    assert_that(
        Account("", "").text(),
        equal_to(""),
        "The account must stay empty for an anonymous upload",
    )
