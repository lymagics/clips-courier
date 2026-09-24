import json
import shutil
from pathlib import Path

import pytest
from hamcrest import assert_that, contains_exactly, equal_to, has_length

from src.domain.fault import Fault
from src.gallery.clip import GalleryClip
from tests.test_fast.fakes import BrokenGallery, FakeGallery


async def test_lists_every_downloaded_picture():
    folder = Path("tmp/test-gallery-clip-album")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/601",
        folder,
        FakeGallery(
            {
                "001.jpg": b"\xff\xd8pic-601-1",
                "002.jpg": b"\xff\xd8pic-601-2",
                "003.jpg": b"\xff\xd8pic-601-3",
            },
            json.dumps({"content": "Three shots", "category": "twitter"}),
        ),
    ).post()
    assert_that(
        post.files(),
        has_length(3),
        "The gallery clip must list every downloaded picture",
    )


async def test_orders_pictures_by_name():
    folder = Path("tmp/test-gallery-clip-order")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/602",
        folder,
        FakeGallery(
            {
                "010.jpg": b"\xff\xd8pic-602-10",
                "002.jpg": b"\xff\xd8pic-602-2",
                "001.jpg": b"\xff\xd8pic-602-1",
            },
            json.dumps({"description": "Ten shots", "category": "instagram"}),
        ),
    ).post()
    assert_that(
        [file.name for file in post.files()],
        contains_exactly("001.jpg", "002.jpg", "010.jpg"),
        "The gallery clip must order the pictures by name",
    )


async def test_leaves_metadata_sidecars_out_of_files():
    folder = Path("tmp/test-gallery-clip-sidecars")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/603",
        folder,
        FakeGallery(
            {"001.png": b"\x89PNGpic-603"},
            json.dumps({"title": "One shot", "category": "tiktok"}),
        ),
    ).post()
    assert_that(
        [file.suffix for file in post.files()],
        contains_exactly(".png"),
        "The gallery clip must leave the metadata sidecars out of the files",
    )


async def test_builds_caption_from_tweet_metadata():
    folder = Path("tmp/test-gallery-clip-tweet")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/604",
        folder,
        FakeGallery(
            {"001.jpg": b"\xff\xd8pic-604"},
            json.dumps(
                {
                    "content": "Sunrise over the ridge 🌄",
                    "description": "alt text of the picture",
                    "author": {"name": "peak_chaser", "nick": "Peak Chaser"},
                    "category": "twitter",
                }
            ),
        ),
    ).post()
    assert_that(
        post.caption(),
        equal_to("Sunrise over the ridge 🌄\n\n— @peak_chaser · X"),
        "The gallery clip must build the caption from the tweet metadata",
    )


async def test_builds_caption_from_instagram_metadata():
    folder = Path("tmp/test-gallery-clip-instagram")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/605",
        folder,
        FakeGallery(
            {"001.jpg": b"\xff\xd8pic-605"},
            json.dumps(
                {
                    "description": "Brunch plate 🥞 #foodie",
                    "username": "fork_and_knife",
                    "fullname": "Fork & Knife",
                    "category": "instagram",
                }
            ),
        ),
    ).post()
    assert_that(
        post.caption(),
        equal_to("Brunch plate 🥞 #foodie\n\n— @fork_and_knife · Instagram"),
        "The gallery clip must build the caption from the instagram metadata",
    )


async def test_builds_caption_from_tiktok_metadata():
    folder = Path("tmp/test-gallery-clip-tiktok")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/606",
        folder,
        FakeGallery(
            {"001.jpeg": b"\xff\xd8pic-606-1", "002.jpeg": b"\xff\xd8pic-606-2"},
            json.dumps(
                {
                    "title": "Slideshow of my cat 🐱",
                    "user": "whisker_wizard",
                    "author": {"uniqueId": "whisker_wizard", "nickname": "Whiskers"},
                    "category": "tiktok",
                }
            ),
        ),
    ).post()
    assert_that(
        post.caption(),
        equal_to("Slideshow of my cat 🐱\n\n— @whisker_wizard · TikTok"),
        "The gallery clip must build the caption from the tiktok metadata",
    )


async def test_falls_back_to_display_name_without_handle():
    folder = Path("tmp/test-gallery-clip-nameless")
    shutil.rmtree(folder, ignore_errors=True)
    post = await GalleryClip(
        "https://example.test/p/607",
        folder,
        FakeGallery(
            {"001.jpg": b"\xff\xd8pic-607"},
            json.dumps(
                {
                    "description": "Untitled",
                    "fullname": "Mystery Poster",
                    "category": "instagram",
                }
            ),
        ),
    ).post()
    assert_that(
        post.caption(),
        equal_to("Untitled\n\n— @Mystery Poster · Instagram"),
        "The gallery clip must fall back to the display name without a handle",
    )


async def test_refuses_link_without_pictures():
    folder = Path("tmp/test-gallery-clip-empty")
    shutil.rmtree(folder, ignore_errors=True)
    with pytest.raises(Fault, match="cannot be downloaded"):
        await GalleryClip(
            "https://example.test/p/608",
            folder,
            FakeGallery({}, json.dumps({"category": "twitter"})),
        ).post()


async def test_reports_failure_of_gallery_tool():
    folder = Path("tmp/test-gallery-clip-broken")
    shutil.rmtree(folder, ignore_errors=True)
    with pytest.raises(Fault, match="cannot be downloaded"):
        await GalleryClip("https://example.test/p/609", folder, BrokenGallery()).post()
