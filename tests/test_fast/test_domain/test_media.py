from pathlib import Path

import pytest
from hamcrest import assert_that, is_

from src.domain.media import Media


@pytest.mark.parametrize(
    "file",
    [
        Path("tmp/test-media/shot-1.jpg"),
        Path("tmp/test-media/shot-2.JPEG"),
        Path("tmp/test-media/shot-3.png"),
        Path("tmp/test-media/shot-4.WebP"),
    ],
)
def test_recognizes_picture_by_suffix(file: Path):
    assert_that(
        Media(file).pictorial(),
        is_(True),
        f"The media must recognize {file.suffix} as a picture",
    )


@pytest.mark.parametrize(
    "file",
    [
        Path("tmp/test-media/clip-5.mp4"),
        Path("tmp/test-media/clip-6.MOV"),
        Path("tmp/test-media/clip-7.webm"),
        Path("tmp/test-media/song-8.mp3"),
        Path("tmp/test-media/noext"),
    ],
)
def test_denies_picture_for_other_suffix(file: Path):
    assert_that(
        Media(file).pictorial(),
        is_(False),
        f"The media must not take {file.name} for a picture",
    )
