from abc import ABC, abstractmethod

from src.domain.stat import Stat


class Downloads(ABC):
    @abstractmethod
    async def record(self, name: str, size: int) -> None:
        pass

    @abstractmethod
    async def tally(self) -> list[Stat]:
        pass
