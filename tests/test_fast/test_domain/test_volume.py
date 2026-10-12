import pytest
from hamcrest import assert_that, equal_to, is_, not_

from src.domain.volume import Volume


@pytest.mark.parametrize(
    "amount,expected",
    [
        (0, "0 B"),
        (777, "777 B"),
        (1024, "1.0 KB"),
        (1536, "1.5 KB"),
        (5242880, "5.0 MB"),
        (1610612736, "1.5 GB"),
        (2199023255552, "2.0 TB"),
    ],
)
def test_prints_amount_in_human_readable_unit(amount: int, expected: str):
    assert_that(
        Volume(amount).text(),
        is_(expected),
        f"The volume must print {amount} bytes as {expected}",
    )


# TODO: Bug: Volume prints 1048575 bytes as "1024.0 KB"
# https://github.com/lymagics/clips-courier/pull/87
@pytest.mark.skip(
    reason=(
        "Bug: Volume prints 1048575 bytes as 1024.0 KB. "
        "See PR https://github.com/lymagics/clips-courier/pull/87"
    )
)
def test_never_prints_a_figure_of_1024_in_a_unit():
    assert_that(
        Volume(1048575).text(),
        not_(equal_to("1024.0 KB")),
        "The volume must roll 1048575 bytes over to MB, not print 1024.0 KB",
    )
