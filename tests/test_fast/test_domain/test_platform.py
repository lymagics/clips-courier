import pytest
from hamcrest import assert_that, equal_to

from src.domain.platform import Platform


@pytest.mark.parametrize(
    "extractor,label",
    [("TikTok", "TikTok"), ("Instagram", "Instagram"), ("Twitter", "X")],
)
def test_prints_friendly_name_for_known_extractor(extractor: str, label: str):
    assert_that(
        Platform(extractor).text(),
        equal_to(label),
        f"The platform must print {extractor} as {label}",
    )


def test_prints_lowercase_extractor_by_canonical_name():
    assert_that(
        Platform("tikTOK").text(),
        equal_to("TikTok"),
        "The platform must print an oddly cased extractor by the canonical name",
    )


def test_falls_back_to_raw_name_for_unknown_extractor():
    assert_that(
        Platform("Dailymotion").text(),
        equal_to("Dailymotion"),
        "The platform must fall back to the raw name for an unknown extractor",
    )
