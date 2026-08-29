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

from src.commands.download import DownloadCommand
from tests.test_fast.fakes import (
    BrokenClip,
    FakeClip,
    FakeClips,
    FakeDownloads,
    FakeMessage,
    FakeUser,
)


async def test_sends_video_from_link():
    folder = Path("tmp/test-download-send")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-311.mp4"
    file.write_bytes(b"\x00\x01video-311")
    message = FakeMessage("/d https://example.test/v/311")
    await DownloadCommand(FakeClips(FakeClip(file)), FakeDownloads({})).answer(message)
    assert_that(
        message.videos,
        has_length(1),
        "The download command must send exactly one video for the link",
    )


async def test_removes_file_after_delivery():
    folder = Path("tmp/test-download-cleanup")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-58.mp4"
    file.write_bytes(b"\xff\xfevideo-58")
    await DownloadCommand(FakeClips(FakeClip(file)), FakeDownloads({})).answer(
        FakeMessage("/d https://example.test/v/58")
    )
    assert_that(
        file.exists(),
        is_(False),
        "The download command must remove the temporary file after delivery",
    )


async def test_answers_downloading_status_before_video():
    folder = Path("tmp/test-download-status")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-91.mp4"
    file.write_bytes(b"\x7fvideo-91")
    message = FakeMessage("/d https://example.test/v/91")
    await DownloadCommand(FakeClips(FakeClip(file)), FakeDownloads({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("Downloading"),
        "The download command must answer with a status before the video",
    )


async def test_answers_short_help_when_link_missing():
    message = FakeMessage("/d")
    await DownloadCommand(FakeClips(BrokenClip()), FakeDownloads({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/d <link>"),
        "The download command must show its usage when no link is given",
    )


async def test_reports_failure_for_broken_link():
    message = FakeMessage("/d https://example.test/gone/9000")
    await DownloadCommand(FakeClips(BrokenClip()), FakeDownloads({})).answer(message)
    assert_that(
        message.replies[-1],
        contains_string("cannot download"),
        "The download command must report a human-friendly failure",
    )


async def test_counts_delivery_toward_sender():
    folder = Path("tmp/test-download-meter")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-777.mp4"
    file.write_bytes(b"\x00\x02video-777")
    downloads = FakeDownloads({})
    await DownloadCommand(FakeClips(FakeClip(file)), downloads).answer(
        FakeMessage("/d https://example.test/v/777", FakeUser(8231, "ivory_shrew"))
    )
    assert_that(
        [stat.name() for stat in await downloads.tally()],
        has_item("ivory_shrew"),
        "The download command must count a delivery toward the sender",
    )


async def test_records_delivered_file_size():
    folder = Path("tmp/test-download-size")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-402.mp4"
    file.write_bytes(b"\x11" * 402)
    downloads = FakeDownloads({})
    await DownloadCommand(FakeClips(FakeClip(file)), downloads).answer(
        FakeMessage("/d https://example.test/v/402", FakeUser(66502, "umber_stork"))
    )
    assert_that(
        [stat.size() for stat in await downloads.tally()],
        has_item(402),
        "The download command must record the size of the delivered file",
    )


async def test_skips_count_for_failed_download():
    downloads = FakeDownloads({})
    await DownloadCommand(FakeClips(BrokenClip()), downloads).answer(
        FakeMessage("/d https://example.test/gone/13", FakeUser(90114, "rosy_finch"))
    )
    assert_that(
        await downloads.tally(),
        has_length(0),
        "The download command must skip the count for a failed download",
    )


async def test_names_sender_without_username_by_id():
    folder = Path("tmp/test-download-nameless")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-55.mp4"
    file.write_bytes(b"\x0avideo-55")
    downloads = FakeDownloads({})
    await DownloadCommand(FakeClips(FakeClip(file)), downloads).answer(
        FakeMessage("/d https://example.test/v/55", FakeUser(31337))
    )
    assert_that(
        [stat.name() for stat in await downloads.tally()],
        has_item("31337"),
        "The download command must name a sender without a username by the id",
    )


def test_builds_aiogram_router():
    assert_that(
        DownloadCommand(FakeClips(BrokenClip()), FakeDownloads({})).router(),
        instance_of(Router),
        "The download command must build an aiogram router",
    )
