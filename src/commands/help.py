from aiogram import Router, filters
from aiogram.types import Message

from src.commands.command import Command
from src.domain.manual import Manual, OwnerManual
from src.domain.reply import Reply


class HelpCommand(Command):
    def __init__(self, name: str, owner: int):
        self.name = name
        self.owner = owner

    def router(self) -> Router:
        router = Router()
        router.message.register(self.answer, filters.Command("h", "help"))
        return router

    async def answer(self, message: Message):
        manual: Reply = Manual(self.name)
        if message.from_user is not None and message.from_user.id == self.owner:
            manual = OwnerManual(manual)
        await message.answer(manual.text())
