from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friend import Friend
from src.domain.friends import Friends
from src.domain.handle import Handle


class RemovalCommand(Command):
    def __init__(self, friends: Friends):
        self.friends = friends

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("kf"))
        return router

    async def answer(self, message: Message):
        words = (message.text or "").split(maxsplit=1)
        if len(words) < 2 or not (words[1].isdigit() or Handle(words[1]).valid()):
            await message.answer(
                "Send the command with a username or an id: /kf @username"
            )
        else:
            await self._expel(message, words[1])

    async def _expel(self, message: Message, word: str):
        found = [
            friend
            for friend in await self.friends.roster()
            if self._matches(friend, word)
        ]
        if found:
            await self.friends.remove(found[0].id())
            await message.answer(
                f"Friend @{found[0].name() or found[0].id()} removed. "
                "They lost access."
            )
        else:
            await message.answer(f"There is no friend {word}. Check the list with /fl")

    def _matches(self, friend: Friend, word: str) -> bool:
        return str(friend.id()) == word or friend.name() == Handle(word).name()
