import shutil
from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to, is_

from src.domain.fault import Fault
from src.domain.tidy import TidyClip
from tests.test_fast.fakes import BrokenClip, FakeClip


async def test_removes_folder_when_file_download_fails():
    folder = Path("tmp/test-tidy-broken-file")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    (folder / "clip-1893.part").write_bytes(b"\x00\x00half-of-1893")
    with pytest.raises(Fault):
        await TidyClip(BrokenClip(), folder).file()
    assert_that(
        folder.exists(),
        is_(False),
        "The tidy clip must remove the folder when the file download fails",
    )


async def test_removes_folder_when_post_download_fails():
    folder = Path("tmp/test-tidy-broken-post")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    (folder / "clip-4172.part").write_bytes(b"\x0f\x0ehalf-of-4172")
    with pytest.raises(Fault):
        await TidyClip(BrokenClip(), folder).post()
    assert_that(
        folder.exists(),
        is_(False),
        "The tidy clip must remove the folder when the post download fails",
    )


async def test_reports_failure_of_origin():
    folder = Path("tmp/test-tidy-missing-folder")
    shutil.rmtree(folder, ignore_errors=True)
    with pytest.raises(Fault, match="broken"):
        await TidyClip(BrokenClip(), folder).file()


async def test_keeps_downloaded_file_in_folder():
    folder = Path("tmp/test-tidy-kept")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-905.mp4"
    file.write_bytes(b"\x19\x05video-905")
    assert_that(
        (await TidyClip(FakeClip(file), folder).file()).read_bytes(),
        equal_to(b"\x19\x05video-905"),
        "The tidy clip must keep the downloaded file in the folder",
    )


async def test_hands_back_post_of_origin():
    folder = Path("tmp/test-tidy-post")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    file = folder / "clip-260.mp4"
    file.write_bytes(b"\x02\x60video-260")
    assert_that(
        (
            await TidyClip(
                FakeClip(file, "Rooftop tango 💃\n\n— @salsa_sky · Instagram"),
                folder,
            ).post()
        ).caption(),
        equal_to("Rooftop tango 💃\n\n— @salsa_sky · Instagram"),
        "The tidy clip must hand back the post of the origin clip",
    )
