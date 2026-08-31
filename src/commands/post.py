import logging

from aiogram import Router, filters
from aiogram.types import FSInputFile, Message

from src.commands.command import Command
from src.domain.clips import Clips
from src.domain.downloads import Downloads
from src.domain.post import Post


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
            await message.answer("Send the command with a link: /dm <link>")
        else:
            await self._deliver(message, words[1])

    async def _deliver(self, message: Message, link: str):
        await message.answer("Downloading…")
        try:
            post = await self.clips.clip(link).post()
        except Exception:
            logging.getLogger(__name__).exception("Download failed: %s", link)
            await message.answer("Sorry, I cannot download this link.")
        else:
            await self._send(message, post)

    async def _send(self, message: Message, post: Post):
        file = post.file()
        try:
            size = file.stat().st_size
            await message.answer_video(FSInputFile(file), caption=post.caption())
            await self._count(message, size)
        finally:
            file.unlink()

    async def _count(self, message: Message, size: int) -> None:
        user = message.from_user
        if user is not None:
            await self.downloads.record(user.username or str(user.id), size)
