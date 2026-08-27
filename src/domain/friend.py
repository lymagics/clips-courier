from abc import ABC, abstractmethod


class Friend(ABC):
    @abstractmethod
    def name(self) -> str:
        pass


class StoredFriend(Friend):
    def __init__(self, name: str):
        self.label = name

    def name(self) -> str:
        return self.label
