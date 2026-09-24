import shutil
from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to, has_length

from src.domain.fallback import FallbackClip
from src.domain.fault import Fault
from tests.test_fast.fakes import BrokenClip, FakeClip


async def test_hands_back_post_of_first_clip():
    folder = Path("tmp/test-fallback-first")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-140.mp4"
    file.write_bytes(b"\x01\x40video-140")
    assert_that(
        (
            await FallbackClip(
                FakeClip([file], "Rain on tin roof 🌧\n\n— @drip_drop · TikTok"),
                BrokenClip(),
            ).post()
        ).caption(),
        equal_to("Rain on tin roof 🌧\n\n— @drip_drop · TikTok"),
        "The fallback clip must hand back the post of the first clip when it works",
    )


async def test_hands_back_post_of_second_clip_when_first_fails():
    folder = Path("tmp/test-fallback-second")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    pictures = [
        folder / "pic-52-1.jpg",
        folder / "pic-52-2.jpg",
        folder / "pic-52-3.jpg",
    ]
    for picture in pictures:
        picture.write_bytes(b"\xff\xd8pic-52")
    assert_that(
        (await FallbackClip(BrokenClip(), FakeClip(pictures)).post()).files(),
        has_length(3),
        "The fallback clip must hand back the second post when the first clip fails",
    )


async def test_reports_failure_when_both_clips_fail():
    with pytest.raises(Fault, match="broken"):
        await FallbackClip(BrokenClip(), BrokenClip()).post()
