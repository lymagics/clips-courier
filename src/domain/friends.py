from abc import ABC, abstractmethod

from src.domain.friend import Friend


class Friends(ABC):
    @abstractmethod
    async def add(self, name: str) -> None:
        pass

    @abstractmethod
    async def remove(self, name: str) -> None:
        pass

    @abstractmethod
    async def roster(self) -> list[Friend]:
        pass
