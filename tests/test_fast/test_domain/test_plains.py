from hamcrest import assert_that, instance_of

from src.domain.plain import PlainClip
from src.domain.plains import PlainClips
from tests.test_fast.fakes import BrokenClip, FakeClips


def test_builds_plain_clip_for_link():
    assert_that(
        PlainClips(FakeClips(BrokenClip())).clip("https://example.test/p/%F0%9F%8E%A5"),
        instance_of(PlainClip),
        "The plain clips must build a clip that drops the caption",
    )
