from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.downloads import Downloads
from src.domain.stat import Stat
from src.domain.volume import Volume


class StatsCommand(Command):
    def __init__(self, downloads: Downloads):
        self.downloads = downloads

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("st", "stats"))
        return router

    async def answer(self, message: Message):
        tally = await self.downloads.tally()
        if tally:
            await message.answer(
                "\n".join(["Downloads:"] + [self._line(stat) for stat in tally])
            )
        else:
            await message.answer("No downloads yet.")

    def _line(self, stat: Stat) -> str:
        return f"{stat.name()} — {stat.count()} ({Volume(stat.size()).text()})"
