import shutil
from pathlib import Path

from aiogram import Router
from hamcrest import (
    assert_that,
    contains_string,
    has_item,
    has_length,
    instance_of,
    is_,
)

from src.commands.post import PostCommand
from tests.test_fast.fakes import (
    BrokenClip,
    FakeClip,
    FakeClips,
    FakeDownloads,
    FakeMessage,
    FakeUser,
)


async def test_sends_caption_together_with_video():
    folder = Path("tmp/test-post-caption")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-612.mp4"
    file.write_bytes(b"\x03\x04video-612")
    message = FakeMessage("/dm https://example.test/v/612")
    await PostCommand(
        FakeClips(FakeClip(file, "Epic gravel rally 🚗\n\n— @gravel_king · TikTok")),
        FakeDownloads({}),
    ).answer(message)
    assert_that(
        message.captions,
        has_item("Epic gravel rally 🚗\n\n— @gravel_king · TikTok"),
        "The post command must send the caption together with the video",
    )


async def test_sends_video_from_link():
    folder = Path("tmp/test-post-send")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-233.mp4"
    file.write_bytes(b"\x05\x06video-233")
    message = FakeMessage("/dm https://example.test/v/233")
    await PostCommand(
        FakeClips(FakeClip(file, "Skate trick 🛹\n\n— @rail_rider · X")),
        FakeDownloads({}),
    ).answer(message)
    assert_that(
        message.videos,
        has_length(1),
        "The post command must send exactly one video for the link",
    )


async def test_removes_file_after_delivery():
    folder = Path("tmp/test-post-cleanup")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-84.mp4"
    file.write_bytes(b"\xfd\xfcvideo-84")
    await PostCommand(
        FakeClips(FakeClip(file, "Beach volley 🏐\n\n— @sand_smash · Instagram")),
        FakeDownloads({}),
    ).answer(FakeMessage("/dm https://example.test/v/84"))
    assert_that(
        file.exists(),
        is_(False),
        "The post command must remove the temporary file after delivery",
    )


async def test_answers_short_help_when_link_missing():
    message = FakeMessage("/dm")
    await PostCommand(FakeClips(BrokenClip()), FakeDownloads({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/dm <link>"),
        "The post command must show its usage when no link is given",
    )


async def test_reports_failure_for_broken_link():
    message = FakeMessage("/dm https://example.test/gone/7100")
    await PostCommand(FakeClips(BrokenClip()), FakeDownloads({})).answer(message)
    assert_that(
        message.replies[-1],
        contains_string("cannot download"),
        "The post command must report a human-friendly failure",
    )


async def test_counts_delivery_toward_sender():
    folder = Path("tmp/test-post-meter")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-951.mp4"
    file.write_bytes(b"\x21" * 951)
    downloads = FakeDownloads({})
    await PostCommand(
        FakeClips(FakeClip(file, "Loud parrot 🦜\n\n— @beak_boss · TikTok")),
        downloads,
    ).answer(
        FakeMessage("/dm https://example.test/v/951", FakeUser(45211, "teal_heron"))
    )
    assert_that(
        [stat.name() for stat in await downloads.tally()],
        has_item("teal_heron"),
        "The post command must count a delivery toward the sender",
    )


def test_builds_aiogram_router():
    assert_that(
        PostCommand(FakeClips(BrokenClip()), FakeDownloads({})).router(),
        instance_of(Router),
        "The post command must build an aiogram router",
    )
