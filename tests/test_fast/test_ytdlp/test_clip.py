import shutil
from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to

from src.domain.fault import Fault
from src.ytdlp.clip import YtdlpClip
from tests.test_fast.fakes import BrokenTool, FakeTool, MetaTool


@pytest.mark.fail_slow("5s")
async def test_downloads_video_into_folder():
    folder = Path("tmp/test-ytdlp-download")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = await YtdlpClip(
        "https://example.test/v/63",
        FakeTool(folder / "clip-63.mp4"),
    ).file()
    assert_that(
        file.read_bytes(),
        equal_to(b"\x00\x00\x00\x18ftypmp42-fake"),
        "The clip must hand back the exact file the tool downloaded",
    )


@pytest.mark.fail_slow("5s")
async def test_refuses_link_without_video():
    with pytest.raises(Fault, match="cannot be downloaded"):
        await YtdlpClip("https://example.test/v/404", BrokenTool()).file()


@pytest.mark.fail_slow("5s")
async def test_builds_post_with_caption_from_metadata():
    folder = Path("tmp/test-ytdlp-meta")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    post = await YtdlpClip(
        "https://example.test/v/44",
        MetaTool(
            folder / "clip-44.mp4",
            {
                "description": "Dancing raccoon 🦝 #wildlife",
                "uploader_id": "trash_panda_tv",
                "uploader": "Trash Panda TV",
                "extractor_key": "TikTok",
            },
        ),
    ).post()
    assert_that(
        post.caption(),
        equal_to("Dancing raccoon 🦝 #wildlife\n\n— @trash_panda_tv · TikTok"),
        "The clip must build a post with a caption from the tool metadata",
    )


@pytest.mark.fail_slow("5s")
async def test_builds_post_with_downloaded_file():
    folder = Path("tmp/test-ytdlp-post")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    post = await YtdlpClip(
        "https://example.test/v/206",
        MetaTool(
            folder / "clip-206.mp4",
            {
                "description": "Foggy morning run 🏃",
                "uploader_id": "misty_miles",
                "extractor_key": "Instagram",
            },
        ),
    ).post()
    assert_that(
        post.file().read_bytes(),
        equal_to(b"\x00\x00\x00\x14ftypisom-meta"),
        "The clip must build a post that points to the downloaded file",
    )


@pytest.mark.fail_slow("5s")
async def test_refuses_post_for_link_without_video():
    with pytest.raises(Fault, match="cannot be downloaded"):
        await YtdlpClip("https://example.test/v/410", BrokenTool()).post()
