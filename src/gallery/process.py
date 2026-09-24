import subprocess
import sys
from pathlib import Path

from src.domain.fault import Fault
from src.gallery.gallery import Gallery


class GalleryProcess(Gallery):
    def __init__(self, options: list[str], timeout: float):
        self.options = options
        self.timeout = timeout

    def fetch(self, link: str, folder: Path) -> None:
        run = subprocess.run(
            [
                sys.executable,
                "-m",
                "gallery_dl",
                "--directory",
                str(folder),
                "--filename",
                "{num:>03}.{extension}",
                "--write-metadata",
                *self.options,
                link,
            ],
            capture_output=True,
            check=False,
            text=True,
            timeout=self.timeout,
        )
        if run.returncode != 0:
            raise Fault(
                f"The gallery tool quit with code {run.returncode}: "
                f"{run.stderr.strip()}"
            )
