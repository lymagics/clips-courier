from abc import ABC, abstractmethod


class Friend(ABC):
    @abstractmethod
    def id(self) -> int:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class StoredFriend(Friend):
    def __init__(self, id: int, name: str):
        self.number = id
        self.label = name

    def id(self) -> int:
        return self.number

    def name(self) -> str:
        return self.label
