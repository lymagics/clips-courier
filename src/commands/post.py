import logging
import shutil

from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.clips import Clips
from src.domain.downloads import Downloads
from src.domain.post import Post
from src.telegram.parcel import Parcel


class PostCommand(Command):
    def __init__(self, clips: Clips, downloads: Downloads):
        self.clips = clips
        self.downloads = downloads

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("dm"))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        if len(words) < 2:
            await message.reply("Send the command with a link: /dm <link>")
        else:
            await self._deliver(message, words[1])

    async def _deliver(self, message: Message, link: str):
        await message.reply("Downloading…")
        try:
            await self._send(message, await self.clips.clip(link).post())
        except Exception:
            logging.getLogger(__name__).exception("Download failed: %s", link)
            await message.reply("Sorry, I cannot download this link.")

    async def _send(self, message: Message, post: Post):
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
