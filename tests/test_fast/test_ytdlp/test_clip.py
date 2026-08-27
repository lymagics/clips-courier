import shutil
import threading
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest
from hamcrest import assert_that, equal_to

from src.domain.fault import Fault
from src.ytdlp.clip import YtdlpClip
from tests.test_fast.fakes import FakeSite


@pytest.mark.fail_slow("5s")
async def test_downloads_video_into_folder():
    folder = Path("tmp/test-ytdlp-download")
    shutil.rmtree(folder, ignore_errors=True)
    (folder / "site").mkdir(parents=True)
    (folder / "site" / "clip-63.mp4").write_bytes(b"\x00\x00\x00\x18ftypmp42-body-63")
    site = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        partial(FakeSite, directory=str(folder / "site")),
    )
    thread = threading.Thread(target=site.serve_forever, daemon=True)
    thread.start()
    try:
        file = await YtdlpClip(
            f"http://127.0.0.1:{site.server_address[1]}/clip-63.mp4",
            folder,
        ).file()
        assert_that(
            file.read_bytes(),
            equal_to(b"\x00\x00\x00\x18ftypmp42-body-63"),
            "The clip must download the exact bytes the site serves",
        )
    finally:
        site.shutdown()
        site.server_close()
        thread.join(timeout=5)


@pytest.mark.fail_slow("5s")
async def test_refuses_link_to_silent_port():
    folder = Path("tmp/test-ytdlp-refusal")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    with pytest.raises(Fault, match="cannot be downloaded"):
        await YtdlpClip("http://127.0.0.1:9/clip-404.mp4", folder).file()
