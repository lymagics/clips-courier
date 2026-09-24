from pathlib import Path

from hamcrest import assert_that, equal_to, instance_of, is_not

from src.domain.clip import Clip
from src.domain.tidy import TidyClip
from src.gallery.clips import GalleryClips
from tests.test_fast.fakes import BrokenGallery


def test_builds_clip_for_link():
    assert_that(
        GalleryClips(Path("tmp/test-gallery-clips-building"), BrokenGallery()).clip(
            "https://example.test/p/17",
        ),
        instance_of(Clip),
        "The gallery clips must build a clip object for the given link",
    )


def test_builds_tidy_clip_for_link():
    assert_that(
        GalleryClips(Path("tmp/test-gallery-clips-tidiness"), BrokenGallery()).clip(
            "https://example.test/p/512",
        ),
        instance_of(TidyClip),
        "The gallery clips must build a clip that cleans its folder up after a failure",
    )


def test_builds_distinct_folder_for_clips_of_one_link():
    clips = GalleryClips(Path("tmp/test-gallery-clips-collision"), BrokenGallery())
    assert_that(
        clips.clip("https://example.test/p/77").folder,
        is_not(equal_to(clips.clip("https://example.test/p/77").folder)),
        "The gallery clips must build a distinct folder for every clip of one link",
    )


def test_nests_clip_folder_inside_own_folder():
    clip = GalleryClips(Path("tmp/test-gallery-clips-nesting"), BrokenGallery()).clip(
        "https://example.test/p/640",
    )
    assert_that(
        clip.folder.parent,
        equal_to(Path("tmp/test-gallery-clips-nesting")),
        "The gallery clips must nest the clip folder inside their own folder",
    )


def test_points_clip_into_folder_it_cleans_up():
    clip = GalleryClips(Path("tmp/test-gallery-clips-pointing"), BrokenGallery()).clip(
        "https://example.test/p/641",
    )
    assert_that(
        clip.origin.folder,
        equal_to(clip.folder),
        "The gallery clips must point the clip into the folder it cleans up",
    )
