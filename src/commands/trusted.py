from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import Router
from aiogram.types import Message

from src.commands.command import Command
from src.domain.friends import Friends


class TrustedCommand(Command):
    def __init__(self, origin: Command, owner: int, friends: Friends):
        self.origin = origin
        self.owner = owner
        self.friends = friends

    def router(self) -> Router:
        router = self.origin.router()
        router.message.middleware(self.guard)
        return router

    async def guard(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> None:
        if await self._trusted(event):
            await handler(event, data)
        else:
            await event.answer("Sorry, access denied.")

    async def _trusted(self, event: Message) -> bool:
        user = event.from_user
        names = [friend.name() for friend in await self.friends.roster()]
        return user is not None and (
            user.id == self.owner or (user.username or "").lower() in names
        )
