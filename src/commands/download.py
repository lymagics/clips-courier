import logging

from aiogram import Router, filters
from aiogram.types import FSInputFile, Message

from src.commands.command import Command
from src.domain.clips import Clips


class DownloadCommand(Command):
    def __init__(self, clips: Clips):
        self.clips = clips

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("d", "download"))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        if len(words) < 2:
            await message.answer("Send the command with a link: /d <link>")
        else:
            await self._deliver(message, words[1])

    async def _deliver(self, message: Message, link: str):
        await message.answer("Downloading…")
        try:
            file = await self.clips.clip(link).file()
        except Exception:
            logging.getLogger(__name__).exception("Download failed: %s", link)
            await message.answer("Sorry, I cannot download this link.")
        else:
            try:
                await message.answer_video(FSInputFile(file))
            finally:
                file.unlink()
