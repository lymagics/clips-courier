from abc import ABC, abstractmethod


class Reply(ABC):
    @abstractmethod
    def text(self) -> str:
        pass
