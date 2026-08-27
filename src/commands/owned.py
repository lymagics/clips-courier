from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import Router
from aiogram.types import Message

from src.commands.command import Command


class OwnedCommand(Command):
    def __init__(self, origin: Command, owner: int):
        self.origin = origin
        self.owner = owner

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
        if event.from_user is not None and event.from_user.id == self.owner:
            await handler(event, data)
        else:
            await event.answer("Sorry, this command works only for the owner.")
