from pathlib import Path

from hamcrest import assert_that, equal_to

from src.domain.post import StoredPost


def test_hands_back_downloaded_file():
    assert_that(
        StoredPost(Path("tmp/test-post-file/clip-909.mp4"), "Boom 💥").file(),
        equal_to(Path("tmp/test-post-file/clip-909.mp4")),
        "The post must hand back the downloaded file",
    )


def test_hands_back_caption_text():
    assert_that(
        StoredPost(
            Path("tmp/test-post-note/clip-17.mp4"),
            "Fireworks finale 🎆\n\n— @sky_writer · X",
        ).caption(),
        equal_to("Fireworks finale 🎆\n\n— @sky_writer · X"),
        "The post must hand back the caption text",
    )
