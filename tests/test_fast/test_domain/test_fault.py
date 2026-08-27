from hamcrest import assert_that, instance_of

from src.domain.fault import Fault


def test_stays_an_ordinary_exception():
    assert_that(
        Fault("The disk is full."),
        instance_of(Exception),
        "The fault must stay an ordinary exception for the top-level recovery",
    )
