from abc import ABC, abstractmethod

from src.domain.post import Post


class Clip(ABC):
    @abstractmethod
    async def post(self) -> Post:
        pass
