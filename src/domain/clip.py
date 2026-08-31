from abc import ABC, abstractmethod
from pathlib import Path

from src.domain.post import Post


class Clip(ABC):
    @abstractmethod
    async def file(self) -> Path:
        pass

    @abstractmethod
    async def post(self) -> Post:
        pass
