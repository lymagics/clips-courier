from pathlib import Path

from hamcrest import assert_that, has_item, has_length, is_

from src.telegram.photo import Photo
from tests.test_fast.fakes import FakeMessage


async def test_replies_with_photo_file():
    message = FakeMessage("/d https://example.test/p/3301")
    await Photo(Path("tmp/test-photo-file/pic-3301.jpg"), "").send(message)
    assert_that(
        message.photos,
        has_length(1),
        "The photo must reply with exactly one photo file",
    )


async def test_attaches_caption_to_photo():
    message = FakeMessage("/dm https://example.test/p/3302")
    await Photo(
        Path("tmp/test-photo-caption/pic-3302.png"),
        "Frozen lake 🧊\n\n— @ice_walker · Instagram",
    ).send(message)
    assert_that(
        message.captions,
        has_item("Frozen lake 🧊\n\n— @ice_walker · Instagram"),
        "The photo must attach the caption to the photo",
    )


async def test_sends_no_caption_for_empty_text():
    message = FakeMessage("/d https://example.test/p/3303")
    await Photo(Path("tmp/test-photo-blank/pic-3303.webp"), "").send(message)
    assert_that(
        message.captions[0],
        is_(None),
        "The photo must send no caption at all when the text is empty",
    )
