import asyncio
from pathlib import Path

from yt_dlp import YoutubeDL

from src.domain.account import Account
from src.domain.caption import Caption
from src.domain.clip import Clip
from src.domain.fault import Fault
from src.domain.platform import Platform
from src.domain.post import Post, StoredPost


class YtdlpClip(Clip):
    def __init__(self, link: str, ytdlp: YoutubeDL):
        self.link = link
        self.ytdlp = ytdlp

    async def file(self) -> Path:
        return (await self.post()).file()

    async def post(self) -> Post:
        try:
            return await asyncio.to_thread(self._post)
        except Exception as e:
            raise Fault("The clip cannot be downloaded.") from e

    def _post(self) -> Post:
        with self.ytdlp as tool:
            info = tool.extract_info(self.link)
        return StoredPost(
            Path(info["requested_downloads"][0]["filepath"]),
            Caption(
                info.get("description") or "",
                Account(
                    info.get("uploader_id") or "",
                    info.get("uploader") or "",
                ).text(),
                Platform(info.get("extractor_key") or "").text(),
            ).text(),
        )
