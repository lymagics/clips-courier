from abc import ABC, abstractmethod

from src.domain.friend import Friend


class Friends(ABC):
    @abstractmethod
    async def add(self, id: int, name: str) -> None:
        pass

    @abstractmethod
    async def remove(self, id: int) -> None:
        pass

    @abstractmethod
    async def roster(self) -> list[Friend]:
        pass
