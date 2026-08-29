from hamcrest import assert_that, is_

from src.domain.stat import StoredStat


def test_keeps_user_name():
    assert_that(
        StoredStat("crimson_ibis", 4, 9001).name(),
        is_("crimson_ibis"),
        "The stored stat must keep the user name",
    )


def test_keeps_download_count():
    assert_that(
        StoredStat("pale_marmot", 17, 63).count(),
        is_(17),
        "The stored stat must keep the download count",
    )


def test_keeps_data_size():
    assert_that(
        StoredStat("quiet_lemur", 2, 40961).size(),
        is_(40961),
        "The stored stat must keep the data size",
    )
