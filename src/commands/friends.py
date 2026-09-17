from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friend import Friend
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
                "\n".join(["Friends:"] + [self._line(friend) for friend in roster])
            )
        else:
            await message.answer("There are no friends yet. Invite one with /f")

    def _line(self, friend: Friend) -> str:
        return (
            f"@{friend.name()} ({friend.id()})" if friend.name() else str(friend.id())
        )
