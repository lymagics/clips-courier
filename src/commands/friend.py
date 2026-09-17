import secrets
import time

from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.invitation import Invitation
from src.domain.invites import Invites


class FriendCommand(Command):
    def __init__(self, invites: Invites, hours: int):
        self.invites = invites
        self.hours = hours

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("f", "friend"))
        return router

    async def answer(self, message: Message):
        token = secrets.token_urlsafe(16)
        await self.invites.add(token, int(time.time()) + self.hours * 3600)
        await message.answer(
            "Send this link to your friend. "
            f"It works once and expires in {self.hours} hours:\n"
            f"{Invitation((await message.bot.me()).username or '', token).text()}"
        )
