from abc import ABC, abstractmethod
from pathlib import Path


class Post(ABC):
    @abstractmethod
    def file(self) -> Path:
        pass

    @abstractmethod
    def caption(self) -> str:
        pass


class StoredPost(Post):
    def __init__(self, file: Path, caption: str):
        self.path = file
        self.note = caption

    def file(self) -> Path:
        return self.path

    def caption(self) -> str:
        return self.note
