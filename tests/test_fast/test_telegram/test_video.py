from pathlib import Path

from hamcrest import assert_that, has_item, has_length, is_

from src.telegram.video import Video
from tests.test_fast.fakes import FakeMessage


async def test_replies_with_video_file():
    message = FakeMessage("/d https://example.test/v/7201")
    await Video(Path("tmp/test-video-file/clip-7201.mp4"), "").send(message)
    assert_that(
        message.videos,
        has_length(1),
        "The video must reply with exactly one video file",
    )


async def test_attaches_caption_to_video():
    message = FakeMessage("/dm https://example.test/v/7202")
    await Video(
        Path("tmp/test-video-caption/clip-7202.mp4"),
        "Windy pier 🌊\n\n— @salt_breeze · X",
    ).send(message)
    assert_that(
        message.captions,
        has_item("Windy pier 🌊\n\n— @salt_breeze · X"),
        "The video must attach the caption to the video",
    )


async def test_sends_no_caption_for_empty_text():
    message = FakeMessage("/d https://example.test/v/7203")
    await Video(Path("tmp/test-video-blank/clip-7203.mp4"), "").send(message)
    assert_that(
        message.captions[0],
        is_(None),
        "The video must send no caption at all when the text is empty",
    )
