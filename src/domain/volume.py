from src.domain.reply import Reply


class Volume(Reply):
    def __init__(self, amount: int):
        self.amount = amount

    def text(self) -> str:
        size = float(self.amount)
        unit = "B"
        for label in ("KB", "MB", "GB", "TB"):
            if size >= 1024.0:
                size = size / 1024.0
                unit = label
        figure = f"{size:g}" if unit == "B" else f"{size:.1f}"
        return f"{figure} {unit}"
