from pathlib import Path

from hamcrest import assert_that, contains_exactly, equal_to

from src.domain.post import StoredPost


def test_hands_back_downloaded_files():
    assert_that(
        StoredPost(
            [
                Path("tmp/test-post-files/pic-909-1.jpg"),
                Path("tmp/test-post-files/pic-909-2.jpg"),
            ],
            "Boom 💥",
        ).files(),
        contains_exactly(
            Path("tmp/test-post-files/pic-909-1.jpg"),
            Path("tmp/test-post-files/pic-909-2.jpg"),
        ),
        "The post must hand back the downloaded files in order",
    )


def test_hands_back_caption_text():
    assert_that(
        StoredPost(
            [Path("tmp/test-post-note/clip-17.mp4")],
            "Fireworks finale 🎆\n\n— @sky_writer · X",
        ).caption(),
        equal_to("Fireworks finale 🎆\n\n— @sky_writer · X"),
        "The post must hand back the caption text",
    )
