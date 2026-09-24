from pathlib import Path


class Media:
    def __init__(self, file: Path):
        self.file = file

    def pictorial(self) -> bool:
        return self.file.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
