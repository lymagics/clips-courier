from abc import ABC, abstractmethod


class Stat(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

    @abstractmethod
    def size(self) -> int:
        pass


class StoredStat(Stat):
    def __init__(self, name: str, count: int, size: int):
        self.label = name
        self.times = count
        self.amount = size

    def name(self) -> str:
        return self.label

    def count(self) -> int:
        return self.times

    def size(self) -> int:
        return self.amount
