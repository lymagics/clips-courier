import asyncio
import logging
from pathlib import Path

from yt_dlp import YoutubeDL

from src.domain.clip import Clip
from src.domain.fault import Fault


class YtdlpClip(Clip):
    def __init__(self, link: str, folder: Path):
        self.link = link
        self.folder = folder

    async def file(self) -> Path:
        try:
            return await asyncio.to_thread(self._downloaded)
        except Exception as e:
            raise Fault("The clip cannot be downloaded.") from e

    def _downloaded(self) -> Path:
        options = {
            "outtmpl": str(self.folder / "%(id)s.%(ext)s"),
            "quiet": True,
            "no_warnings": True,
            "noprogress": True,
            "retries": 3,
            "socket_timeout": 30,
            "logger": logging.getLogger("yt_dlp"),
        }
        with YoutubeDL(options) as tool:
            info = tool.extract_info(self.link)
        return Path(info["requested_downloads"][0]["filepath"])
