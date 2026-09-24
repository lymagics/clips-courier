from pathlib import Path

from hamcrest import assert_that, has_item, has_length

from src.telegram.parcel import Parcel
from tests.test_fast.fakes import FakeMessage


async def test_sends_lone_clip_as_video():
    message = FakeMessage("/d https://example.test/v/5501")
    await Parcel([Path("tmp/test-parcel-video/clip-5501.mp4")], "").send(message)
    assert_that(
        message.videos,
        has_length(1),
        "The parcel must send a lone clip as a video",
    )


async def test_sends_lone_picture_as_photo():
    message = FakeMessage("/d https://example.test/p/5502")
    await Parcel([Path("tmp/test-parcel-photo/pic-5502.jpg")], "").send(message)
    assert_that(
        message.photos,
        has_length(1),
        "The parcel must send a lone picture as a photo",
    )


async def test_sends_several_pictures_as_album():
    message = FakeMessage("/d https://example.test/p/5503")
    await Parcel(
        [
            Path("tmp/test-parcel-album/pic-5503-1.jpg"),
            Path("tmp/test-parcel-album/pic-5503-2.png"),
            Path("tmp/test-parcel-album/pic-5503-3.webp"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums,
        has_length(1),
        "The parcel must send several pictures as one album",
    )


async def test_passes_caption_along_with_photo():
    message = FakeMessage("/dm https://example.test/p/5504")
    await Parcel(
        [Path("tmp/test-parcel-caption/pic-5504.jpg")],
        "Old lighthouse 🗼\n\n— @beam_keeper · Instagram",
    ).send(message)
    assert_that(
        message.captions,
        has_item("Old lighthouse 🗼\n\n— @beam_keeper · Instagram"),
        "The parcel must pass the caption along with the photo",
    )
