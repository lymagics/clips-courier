from pathlib import Path

from hamcrest import assert_that, instance_of

from src.domain.clip import Clip
from src.ytdlp.clips import YtdlpClips


def test_builds_clip_for_link():
    assert_that(
        YtdlpClips(Path("tmp")).clip("https://example.test/v/17"),
        instance_of(Clip),
        "The clips must build a clip object for the given link",
    )
