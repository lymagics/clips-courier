from pathlib import Path

from aiogram.types import InputMediaPhoto, InputMediaVideo
from hamcrest import (
    assert_that,
    contains_exactly,
    equal_to,
    has_length,
    instance_of,
    is_,
    only_contains,
)

from src.telegram.album import Album
from tests.test_fast.fakes import FakeMessage


async def test_replies_with_one_media_group_for_three_pictures():
    message = FakeMessage("/d https://example.test/p/4401")
    await Album(
        [
            Path("tmp/test-album-three/pic-4401-1.jpg"),
            Path("tmp/test-album-three/pic-4401-2.jpg"),
            Path("tmp/test-album-three/pic-4401-3.jpg"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums,
        has_length(1),
        "The album must reply with one media group for three pictures",
    )


async def test_keeps_every_picture_in_the_group():
    message = FakeMessage("/d https://example.test/p/4402")
    await Album(
        [
            Path("tmp/test-album-size/pic-4402-1.png"),
            Path("tmp/test-album-size/pic-4402-2.png"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums[0],
        has_length(2),
        "The album must keep every picture in the media group",
    )


async def test_wraps_pictures_as_photos():
    message = FakeMessage("/d https://example.test/p/4403")
    await Album(
        [
            Path("tmp/test-album-kind/pic-4403-1.webp"),
            Path("tmp/test-album-kind/pic-4403-2.jpeg"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums[0],
        only_contains(instance_of(InputMediaPhoto)),
        "The album must wrap the pictures as photos",
    )


async def test_wraps_clip_among_pictures_as_video():
    message = FakeMessage("/d https://example.test/p/4404")
    await Album(
        [
            Path("tmp/test-album-mixed/pic-4404-1.jpg"),
            Path("tmp/test-album-mixed/clip-4404-2.mp4"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums[0][1],
        instance_of(InputMediaVideo),
        "The album must wrap a clip among the pictures as a video",
    )


async def test_puts_caption_on_first_item_only():
    message = FakeMessage("/dm https://example.test/p/4405")
    await Album(
        [
            Path("tmp/test-album-caption/pic-4405-1.jpg"),
            Path("tmp/test-album-caption/pic-4405-2.jpg"),
        ],
        "Street mural 🎨\n\n— @wall_crawler · X",
    ).send(message)
    assert_that(
        [item.caption for item in message.albums[0]],
        contains_exactly("Street mural 🎨\n\n— @wall_crawler · X", None),
        "The album must put the caption on the first item only",
    )


async def test_sends_no_caption_for_empty_text():
    message = FakeMessage("/d https://example.test/p/4406")
    await Album(
        [
            Path("tmp/test-album-blank/pic-4406-1.jpg"),
            Path("tmp/test-album-blank/pic-4406-2.jpg"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums[0][0].caption,
        is_(None),
        "The album must send no caption at all when the text is empty",
    )


async def test_splits_long_slideshow_into_telegram_sized_groups():
    message = FakeMessage("/d https://example.test/p/4407")
    await Album(
        [Path(f"tmp/test-album-long/pic-4407-{n:02}.jpg") for n in range(1, 24)],
        "",
    ).send(message)
    assert_that(
        [len(group) for group in message.albums],
        contains_exactly(10, 10, 3),
        "The album must split a long slideshow into groups of at most ten items",
    )


async def test_keeps_caption_on_first_group_only():
    message = FakeMessage("/dm https://example.test/p/4408")
    await Album(
        [Path(f"tmp/test-album-long-caption/pic-4408-{n:02}.jpg") for n in range(12)],
        "Twelve steps 🪜\n\n— @stair_master · TikTok",
    ).send(message)
    assert_that(
        message.albums[1][0].caption,
        is_(None),
        "The album must keep the caption on the first group only",
    )


async def test_points_items_to_given_files():
    message = FakeMessage("/d https://example.test/p/4409")
    await Album(
        [
            Path("tmp/test-album-paths/pic-4409-1.jpg"),
            Path("tmp/test-album-paths/pic-4409-2.jpg"),
        ],
        "",
    ).send(message)
    assert_that(
        message.albums[0][1].media.path,
        equal_to(Path("tmp/test-album-paths/pic-4409-2.jpg")),
        "The album must point every item to the given file",
    )
