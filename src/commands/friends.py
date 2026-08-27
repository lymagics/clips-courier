from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friends import Friends


class FriendsCommand(Command):
    def __init__(self, friends: Friends):
        self.friends = friends

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("fl", "friends"))
        return router

    async def answer(self, message: Message):
        roster = await self.friends.roster()
        if roster:
            await message.answer(
                "\n".join(["Friends:"] + [f"@{friend.name()}" for friend in roster])
            )
        else:
            await message.answer("There are no friends yet. Add one with /f @username")
