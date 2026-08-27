from abc import ABC, abstractmethod

from src.domain.clip import Clip


class Clips(ABC):
    @abstractmethod
    def clip(self, link: str) -> Clip:
        pass
