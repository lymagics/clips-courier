from abc import ABC, abstractmethod

from aiogram import Router


class Command(ABC):
    @abstractmethod
    def router(self) -> Router:
        pass
