import shutil
from pathlib import Path

from aiogram import Router
from hamcrest import assert_that, contains_string, has_length, instance_of, is_

from src.commands.download import DownloadCommand
from tests.test_fast.fakes import BrokenClip, FakeClip, FakeClips, FakeMessage


async def test_sends_video_from_link():
    folder = Path("tmp/test-download-send")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-311.mp4"
    file.write_bytes(b"\x00\x01video-311")
    message = FakeMessage("/d https://example.test/v/311")
    await DownloadCommand(FakeClips(FakeClip(file))).answer(message)
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
    await DownloadCommand(FakeClips(FakeClip(file))).answer(
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
    await DownloadCommand(FakeClips(FakeClip(file))).answer(message)
    assert_that(
        message.replies[0],
        contains_string("Downloading"),
        "The download command must answer with a status before the video",
    )


async def test_answers_short_help_when_link_missing():
    message = FakeMessage("/d")
    await DownloadCommand(FakeClips(BrokenClip())).answer(message)
    assert_that(
        message.replies[0],
        contains_string("/d <link>"),
        "The download command must show its usage when no link is given",
    )


async def test_reports_failure_for_broken_link():
    message = FakeMessage("/d https://example.test/gone/9000")
    await DownloadCommand(FakeClips(BrokenClip())).answer(message)
    assert_that(
        message.replies[-1],
        contains_string("cannot download"),
        "The download command must report a human-friendly failure",
    )


def test_builds_aiogram_router():
    assert_that(
        DownloadCommand(FakeClips(BrokenClip())).router(),
        instance_of(Router),
        "The download command must build an aiogram router",
    )
