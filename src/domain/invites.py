from abc import ABC, abstractmethod


class Invites(ABC):
    @abstractmethod
    async def add(self, token: str, deadline: int) -> None:
        pass

    @abstractmethod
    async def remove(self, token: str) -> None:
        pass

    @abstractmethod
    async def valid(self, token: str, now: int) -> bool:
        pass
