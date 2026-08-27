from src.domain.reply import Reply


class Greeting(Reply):
    def __init__(self, name: str):
        self.name = name

    def text(self) -> str:
        return (
            f"Hi! I am {self.name or 'Clips Courier'}.\n"
            "I deliver short videos right into this chat.\n"
            "Send /h to see what I can do."
        )
