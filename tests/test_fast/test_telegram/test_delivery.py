import shutil
from pathlib import Path

from aiogram.types import FSInputFile
from hamcrest import assert_that, contains_string, has_item, has_length, is_

from src.telegram.delivery import Delivery
from tests.test_fast.fakes import (
    BrokenClip,
    FakeClip,
    FakeClips,
    FakeDownloads,
    FakeMessage,
    FakeUser,
)


class RejectingMessage(FakeMessage):
    async def reply_video(self, video: FSInputFile, caption: str | None = None):
        raise RuntimeError("Telegram refused the delivered video for its size.")


async def test_replies_with_downloading_status_first():
    folder = Path("tmp/test-delivery-status")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-1730.mp4"
    file.write_bytes(b"\x17\x30video-1730")
    message = FakeMessage("/d https://example.test/v/1730")
    await Delivery(
        "https://example.test/v/1730",
        FakeClips(FakeClip([file])),
        FakeDownloads({}),
    ).send(message)
    assert_that(
        message.quoted[0],
        contains_string("Downloading"),
        "The delivery must reply with the downloading status before anything else",
    )


async def test_sends_caption_of_post():
    folder = Path("tmp/test-delivery-caption")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-4096.mp4"
    file.write_bytes(b"\x40\x96video-4096")
    message = FakeMessage("/dm https://example.test/v/4096")
    await Delivery(
        "https://example.test/v/4096",
        FakeClips(FakeClip([file], "Snowy owl 🦉 — «hoo»\n\n— @night_wing · X")),
        FakeDownloads({}),
    ).send(message)
    assert_that(
        message.captions,
        has_item("Snowy owl 🦉 — «hoo»\n\n— @night_wing · X"),
        "The delivery must send the caption of the post",
    )


async def test_removes_folder_after_sending():
    folder = Path("tmp/test-delivery-cleanup")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-0.mp4"
    file.write_bytes(b"")
    await Delivery(
        "https://example.test/v/0",
        FakeClips(FakeClip([file])),
        FakeDownloads({}),
    ).send(FakeMessage("/d https://example.test/v/0"))
    assert_that(
        folder.exists(),
        is_(False),
        "The delivery must remove the temporary folder after sending",
    )


async def test_removes_folder_when_telegram_rejects_the_video():
    folder = Path("tmp/test-delivery-rejected-cleanup")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-6144.mp4"
    file.write_bytes(b"\x61\x44" * 77)
    await Delivery(
        "https://example.test/v/6144",
        FakeClips(FakeClip([file])),
        FakeDownloads({}),
    ).send(RejectingMessage("/d https://example.test/v/6144"))
    assert_that(
        folder.exists(),
        is_(False),
        "The delivery must remove the temporary folder when telegram rejects it",
    )


async def test_reports_failure_when_telegram_rejects_the_video():
    folder = Path("tmp/test-delivery-rejected")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-8192.mp4"
    file.write_bytes(b"\x81\x92" * 63)
    message = RejectingMessage("/d https://example.test/v/8192")
    await Delivery(
        "https://example.test/v/8192",
        FakeClips(FakeClip([file])),
        FakeDownloads({}),
    ).send(message)
    assert_that(
        message.quoted[-1],
        contains_string("cannot download"),
        "The delivery must report a failure when telegram rejects the video",
    )


async def test_skips_count_when_telegram_rejects_the_video():
    folder = Path("tmp/test-delivery-rejected-count")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-2048.mp4"
    file.write_bytes(b"\x20\x48" * 19)
    downloads = FakeDownloads({})
    await Delivery(
        "https://example.test/v/2048",
        FakeClips(FakeClip([file])),
        downloads,
    ).send(
        RejectingMessage("/d https://example.test/v/2048", FakeUser(2048, "dusk_lynx"))
    )
    assert_that(
        await downloads.tally(),
        has_length(0),
        "The delivery must skip the count when telegram rejects the video",
    )


async def test_reports_failure_for_broken_clip():
    message = FakeMessage("/d https://example.test/gone/1")
    await Delivery(
        "https://example.test/gone/1",
        FakeClips(BrokenClip()),
        FakeDownloads({}),
    ).send(message)
    assert_that(
        message.quoted[-1],
        contains_string("cannot download"),
        "The delivery must report a human-friendly failure for a broken clip",
    )


async def test_records_size_toward_sender():
    folder = Path("tmp/test-delivery-size")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    pictures = [folder / f"pic-1999-{n}.jpg" for n in (1, 2)]
    pictures[0].write_bytes(b"\xff" * 1000)
    pictures[1].write_bytes(b"\xd8" * 999)
    downloads = FakeDownloads({})
    await Delivery(
        "https://example.test/p/1999",
        FakeClips(FakeClip(pictures)),
        downloads,
    ).send(FakeMessage("/d https://example.test/p/1999", FakeUser(1999, "ash_vole")))
    assert_that(
        [(stat.name(), stat.size()) for stat in await downloads.tally()],
        has_item(("ash_vole", 1999)),
        "The delivery must record the whole size toward the sender",
    )


async def test_names_sender_without_username_by_id():
    folder = Path("tmp/test-delivery-nameless")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-7.mp4"
    file.write_bytes(b"\x07video-7")
    downloads = FakeDownloads({})
    await Delivery(
        "https://example.test/v/7",
        FakeClips(FakeClip([file])),
        downloads,
    ).send(FakeMessage("/d https://example.test/v/7", FakeUser(9007199254740993)))
    assert_that(
        [stat.name() for stat in await downloads.tally()],
        has_item("9007199254740993"),
        "The delivery must name a sender without a username by the id",
    )
