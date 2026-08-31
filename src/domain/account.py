from src.domain.reply import Reply


class Account(Reply):
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name

    def text(self) -> str:
        handle = self.id.strip()
        return self.name.strip() if not handle or handle.isdigit() else handle
