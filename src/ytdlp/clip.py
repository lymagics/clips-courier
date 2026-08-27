import asyncio
from pathlib import Path

from yt_dlp import YoutubeDL

from src.domain.clip import Clip
from src.domain.fault import Fault


class YtdlpClip(Clip):
    def __init__(self, link: str, ytdlp: YoutubeDL):
        self.link = link
        self.ytdlp = ytdlp

    async def file(self) -> Path:
        try:
            return await asyncio.to_thread(self._downloaded)
        except Exception as e:
            raise Fault("The clip cannot be downloaded.") from e

    def _downloaded(self) -> Path:
        with self.ytdlp as tool:
            info = tool.extract_info(self.link)
        return Path(info["requested_downloads"][0]["filepath"])
