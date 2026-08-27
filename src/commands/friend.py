from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friends import Friends
from src.domain.handle import Handle


class FriendCommand(Command):
    def __init__(self, friends: Friends):
        self.friends = friends

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("f", "friend"))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        if len(words) < 2 or not Handle(words[1]).valid():
            await message.answer("Send the command with a username: /f @username")
        else:
            await self._admit(message, Handle(words[1]).name())

    async def _admit(self, message: Message, name: str):
        await self.friends.add(name)
        await message.answer(f"Friend @{name} added. They can download clips now.")
