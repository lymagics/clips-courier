from hamcrest import assert_that, equal_to

from src.domain.friend import StoredFriend


def test_tells_its_username():
    assert_that(
        StoredFriend("velvet_moth").name(),
        equal_to("velvet_moth"),
        "The stored friend must tell its username",
    )
