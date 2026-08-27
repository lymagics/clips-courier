from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friends import Friends
from src.domain.handle import Handle


class RemovalCommand(Command):
    def __init__(self, friends: Friends):
        self.friends = friends

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("r", "remove"))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        if len(words) < 2 or not Handle(words[1]).valid():
            await message.answer("Send the command with a username: /r @username")
        else:
            await self._expel(message, Handle(words[1]).name())

    async def _expel(self, message: Message, name: str):
        await self.friends.remove(name)
        await message.answer(f"Friend @{name} removed. They lost access.")
