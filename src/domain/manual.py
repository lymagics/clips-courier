from src.domain.reply import Reply


class OwnerManual(Reply):
    def __init__(self, origin: Reply):
        self.origin = origin

    def text(self) -> str:
        return (
            f"{self.origin.text()}\n"
            "/f @username — add a friend\n"
            "/fl — show the friend list\n"
            "/kf @username — remove a friend\n"
            "/st — show download statistics"
        )


class Manual(Reply):
    def __init__(self, name: str):
        self.name = name

    def text(self) -> str:
        return "\n".join(
            (
                f"{self.name or 'Clips Courier'} understands these commands:",
                "/s — show the welcome message",
                "/h — show this help",
                "/d <link> — download the video and send it here",
            )
        )
