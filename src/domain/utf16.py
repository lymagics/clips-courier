class Utf16Text:
    def __init__(self, src: str):
        self.src = src

    def units(self) -> int:
        return len(self.src.encode("utf-16-le")) // 2

    def clipped(self, room: int) -> str:
        return self.src.encode("utf-16-le")[: max(room, 0) * 2].decode(
            "utf-16-le", errors="ignore"
        )
