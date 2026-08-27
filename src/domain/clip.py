from abc import ABC, abstractmethod
from pathlib import Path


class Clip(ABC):
    @abstractmethod
    async def file(self) -> Path:
        pass
