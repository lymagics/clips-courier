from src.domain.reply import Reply


class Invitation(Reply):
    def __init__(self, bot: str, token: str):
        self.bot = bot
        self.token = token

    def text(self) -> str:
        return f"https://t.me/{self.bot}?start={self.token}"
