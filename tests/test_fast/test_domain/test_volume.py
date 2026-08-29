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
