from src.domain.reply import Reply


class Caption(Reply):
    def __init__(self, description: str, account: str, platform: str):
        self.description = description
        self.account = account
        self.platform = platform

    def text(self) -> str:
        footer = self._footer()
        room = max(0, 1022 - len(footer))
        body = self._body(room)
        return f"{body}\n\n{footer}" if body else footer

    def _footer(self) -> str:
        name = self.account.strip().removeprefix("@")
        if name:
            overhead = len("— @") + len(f" · {self.platform}")
            name = name[: max(0, 1022 - overhead)]
            return f"— @{name} · {self.platform}"
        return f"— {self.platform}"

    def _clipped(self, text: str, room: int) -> str:
        return (
            text
            if len(text) <= room
            else text[: room - 1].rstrip() + "…" if room > 0 else ""
        )
