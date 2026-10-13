import pytest
from hamcrest import assert_that, is_

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


@pytest.mark.parametrize(
    "amount,expected",
    [
        (1048525, "1.0 MB"),
        (1048575, "1.0 MB"),
        (1073741823, "1.0 GB"),
        (1099511627775, "1.0 TB"),
    ],
)
def test_rolls_over_to_next_unit_when_figure_rounds_to_1024(amount: int, expected: str):
    assert_that(
        Volume(amount).text(),
        is_(expected),
        f"The volume must roll {amount} bytes over to {expected}, not print 1024.0",
    )


def test_keeps_unit_when_figure_rounds_below_1024():
    assert_that(
        Volume(1048524).text(),
        is_("1023.9 KB"),
        "The volume must print 1048524 bytes as 1023.9 KB",
    )
