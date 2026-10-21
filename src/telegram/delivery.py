import logging
import shutil

from aiogram.types import Message

from src.domain.clips import Clips
from src.domain.downloads import Downloads
from src.domain.post import Post
from src.telegram.attachment import Attachment
from src.telegram.parcel import Parcel


class Delivery(Attachment):
    def __init__(self, link: str, clips: Clips, downloads: Downloads):
        self.link = link
        self.clips = clips
        self.downloads = downloads

    async def send(self, message: Message) -> None:
        await message.reply("Downloading…")
        try:
            await self._ship(message, await self.clips.clip(self.link).post())
        except Exception:
            logging.getLogger(__name__).exception("Download failed: %s", self.link)
            await message.reply("Sorry, I cannot download this link.")

    async def _ship(self, message: Message, post: Post):
        files = post.files()
        try:
            size = sum(file.stat().st_size for file in files)
            await Parcel(files, post.caption()).send(message)
            await self._count(message, size)
        finally:
            for folder in {file.parent for file in files}:
                shutil.rmtree(folder)

    async def _count(self, message: Message, size: int) -> None:
        user = message.from_user
        if user is not None:
            await self.downloads.record(user.username or str(user.id), size)
