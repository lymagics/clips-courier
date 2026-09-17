from hamcrest import assert_that, equal_to

from src.domain.friend import StoredFriend


def test_tells_its_username():
    assert_that(
        StoredFriend(48117, "velvet_moth").name(),
        equal_to("velvet_moth"),
        "The stored friend must tell its username",
    )


def test_tells_its_telegram_id():
    assert_that(
        StoredFriend(90210311, "tin_crane").id(),
        equal_to(90210311),
        "The stored friend must tell its telegram id",
    )
