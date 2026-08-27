import re


class Handle:
    def __init__(self, src: str):
        self.src = src

    def name(self) -> str:
        return self.src.strip().removeprefix("@").lower()

    def valid(self) -> bool:
        return re.fullmatch(r"[a-z0-9_]{5,32}", self.name()) is not None
