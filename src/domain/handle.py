import re


class Handle:
    def __init__(self, src: str):
        self.src = src

    def name(self) -> str:
        return self.src.strip().removeprefix("@").lower()

    def valid(self) -> bool:
        return re.fullmatch(r"[a-z][a-z0-9_]{4,31}", self.name()) is not None
