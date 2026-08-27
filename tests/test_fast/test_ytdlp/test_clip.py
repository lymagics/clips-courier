import shutil
from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to

from src.domain.fault import Fault
from src.ytdlp.clip import YtdlpClip
from tests.test_fast.fakes import BrokenTool, FakeTool


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
