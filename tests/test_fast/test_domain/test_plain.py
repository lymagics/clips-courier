import shutil
from pathlib import Path

from hamcrest import assert_that, empty, equal_to

from src.domain.plain import PlainClip
from tests.test_fast.fakes import FakeClip


async def test_drops_caption_of_origin():
    folder = Path("tmp/test-plain-caption")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-3141.mp4"
    file.write_bytes(b"\x31\x41video-3141")
    assert_that(
        (
            await PlainClip(
                FakeClip([file], "Pi day bake-off 🥧\n\n— @crust_lord · TikTok")
            ).post()
        ).caption(),
        empty(),
        "The plain clip must drop the caption of the origin clip",
    )


async def test_keeps_files_of_origin():
    folder = Path("tmp/test-plain-files")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    pictures = [folder / f"pic-2718-{n}.webp" for n in (1, 2)]
    for picture in pictures:
        picture.write_bytes(b"RIFF\x27\x18WEBP")
    assert_that(
        (await PlainClip(FakeClip(pictures, "Euler's ferns 🌿")).post()).files(),
        equal_to(pictures),
        "The plain clip must keep the files of the origin clip",
    )
