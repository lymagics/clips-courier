from src.domain.reply import Reply
from src.domain.utf16 import Utf16Text


class Caption(Reply):
    def __init__(self, description: str, account: str, platform: str):
        self.description = description
        self.account = account
        self.platform = platform

    def text(self) -> str:
        footer = self._clipped(self._footer(), 1024)
        body = self._clipped(
            self.description.strip(),
            1022 - Utf16Text(footer).units(),
        )
        return f"{body}\n\n{footer}" if body else footer

    def _footer(self) -> str:
        name = self.account.strip().removeprefix("@")
        return f"— @{name} · {self.platform}" if name else f"— {self.platform}"

    def _clipped(self, text: str, room: int) -> str:
        return (
            text
            if Utf16Text(text).units() <= room
            else Utf16Text(text).clipped(room - 1).rstrip() + "…" if room > 0 else ""
        )
