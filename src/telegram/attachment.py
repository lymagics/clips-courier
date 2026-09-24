from abc import ABC, abstractmethod

from aiogram.types import Message


class Attachment(ABC):
    @abstractmethod
    async def send(self, message: Message) -> None:
        pass
