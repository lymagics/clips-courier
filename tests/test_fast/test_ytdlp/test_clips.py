from pathlib import Path

from hamcrest import assert_that, equal_to, instance_of, is_not, same_instance

from src.domain.clip import Clip
from src.domain.tidy import TidyClip
from src.ytdlp.clips import YtdlpClips


def test_builds_clip_for_link():
    assert_that(
        YtdlpClips(Path("tmp/test-clips-building"), {"quiet": True}).clip(
            "https://example.test/v/17",
        ),
        instance_of(Clip),
        "The clips must build a clip object for the given link",
    )


def test_builds_fresh_tool_for_every_clip():
    clips = YtdlpClips(Path("tmp/test-clips-freshness"), {"noprogress": True})
    assert_that(
        clips.clip("https://example.test/v/29").origin.ytdlp,
        is_not(same_instance(clips.clip("https://example.test/v/31").origin.ytdlp)),
        "The clips must build a fresh tool for every clip",
    )


def test_builds_distinct_folder_for_clips_of_one_link():
    clips = YtdlpClips(Path("tmp/test-clips-collision"), {"quiet": True})
    assert_that(
        clips.clip("https://example.test/v/77").folder,
        is_not(equal_to(clips.clip("https://example.test/v/77").folder)),
        "The clips must build a distinct folder for every clip of one link",
    )


def test_builds_tidy_clip_for_link():
    assert_that(
        YtdlpClips(Path("tmp/test-clips-tidiness"), {"quiet": True}).clip(
            "https://example.test/v/512",
        ),
        instance_of(TidyClip),
        "The clips must build a clip that cleans its folder up after a failure",
    )


def test_points_tool_into_clip_folder():
    clip = YtdlpClips(Path("tmp/test-clips-nesting"), {"quiet": True}).clip(
        "https://example.test/v/640",
    )
    assert_that(
        Path(clip.origin.ytdlp.params["outtmpl"]["default"]).parent,
        equal_to(clip.folder),
        "The clips must point the tool into the folder the clip cleans up",
    )
