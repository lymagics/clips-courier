from abc import ABC, abstractmethod
from pathlib import Path


class Gallery(ABC):
    @abstractmethod
    def fetch(self, link: str, folder: Path) -> None:
        pass
