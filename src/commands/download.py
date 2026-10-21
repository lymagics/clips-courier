from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.clips import Clips
from src.domain.downloads import Downloads
from src.domain.plains import PlainClips
from src.telegram.delivery import Delivery


class DownloadCommand(Command):
    def __init__(self, clips: Clips, downloads: Downloads):
        self.clips = clips
        self.downloads = downloads

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("d", "download"))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        if len(words) < 2:
            await message.reply("Send the command with a link: /d <link>")
        else:
            await Delivery(words[1], PlainClips(self.clips), self.downloads).send(
                message
            )
