from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.greeting import Greeting


class StartCommand(Command):
    def __init__(self, name: str):
        self.name = name

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("s", "start"))
        return router

    async def answer(self, message: Message):
        await message.answer(Greeting(self.name).text())
