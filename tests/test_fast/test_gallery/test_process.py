import shutil
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

import pytest
from hamcrest import assert_that, equal_to

from src.domain.fault import Fault
from src.gallery.process import GalleryProcess


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.mark.fail_slow("10s")
def test_refuses_unsupported_link():
    folder = Path("tmp/test-gallery-process-unsupported")
    shutil.rmtree(folder, ignore_errors=True)
    with pytest.raises(Fault, match="Unsupported URL"):
        GalleryProcess([], 30).fetch("https://example.test/nothing/12", folder)


@pytest.mark.fail_slow("10s")
def test_downloads_picture_into_folder():
    site = Path("tmp/test-gallery-process-site")
    shutil.rmtree(site, ignore_errors=True)
    site.mkdir(parents=True)
    (site / "pic-77.jpg").write_bytes(b"\xff\xd8\xff\xe0jpeg-77")
    folder = Path("tmp/test-gallery-process-folder")
    shutil.rmtree(folder, ignore_errors=True)
    server = ThreadingHTTPServer(
        ("127.0.0.1", 0),
        lambda *args: QuietHandler(*args, directory=str(site)),
    )
    Thread(target=server.serve_forever, daemon=True).start()
    try:
        GalleryProcess([], 30).fetch(
            f"http://127.0.0.1:{server.server_address[1]}/pic-77.jpg", folder
        )
    finally:
        server.shutdown()
        server.server_close()
    assert_that(
        next(folder.glob("*.jpg")).read_bytes(),
        equal_to(b"\xff\xd8\xff\xe0jpeg-77"),
        "The gallery process must download the picture into the folder",
    )
