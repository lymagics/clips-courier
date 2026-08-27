from aiogram import Bot as Telegram
from aiogram import Dispatcher

from src.commands.command import Command


class Bot:
    def __init__(self, *commands: Command):
        self.commands = commands

    def bot(self, token: str) -> Dispatcher:
        dispatcher = Dispatcher()
        dispatcher["courier"] = Telegram(token)
        for command in self.commands:
            dispatcher.include_router(command.router())
        return dispatcher
