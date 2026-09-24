from abc import ABC, abstractmethod
from pathlib import Path


class Post(ABC):
    @abstractmethod
    def files(self) -> list[Path]:
        pass

    @abstractmethod
    def caption(self) -> str:
        pass


class StoredPost(Post):
    def __init__(self, files: list[Path], caption: str):
        self.paths = files
        self.note = caption

    def files(self) -> list[Path]:
        return list(self.paths)

    def caption(self) -> str:
        return self.note
