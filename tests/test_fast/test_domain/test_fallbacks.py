from hamcrest import assert_that, instance_of

from src.domain.fallback import FallbackClip
from src.domain.fallbacks import FallbackClips
from tests.test_fast.fakes import BrokenClip, FakeClips


def test_builds_fallback_clip_for_link():
    assert_that(
        FallbackClips(FakeClips(BrokenClip()), FakeClips(BrokenClip())).clip(
            "https://example.test/p/8801"
        ),
        instance_of(FallbackClip),
        "The fallback clips must build a clip that falls back to the second backend",
    )
