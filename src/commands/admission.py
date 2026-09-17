import time

from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friends import Friends
from src.domain.invites import Invites


class AdmissionCommand(Command):
    def __init__(self, invites: Invites, friends: Friends):
        self.invites = invites
        self.friends = friends

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.CommandStart(deep_link=True))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        token = words[1] if len(words) > 1 else ""
        user = message.from_user
        if user is not None and await self.invites.valid(token, int(time.time())):
            await self.invites.remove(token)
            await self.friends.add(user.id, (user.username or "").lower())
            await message.answer(
                "Welcome! You can download clips now. Send /h to see the commands."
            )
        else:
            await message.answer(
                "Sorry, this invitation link is invalid or has expired."
            )
