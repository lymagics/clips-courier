from src.domain.reply import Reply


class Platform(Reply):
    def __init__(self, extractor: str):
        self.extractor = extractor

    def text(self) -> str:
        titles = {"tiktok": "TikTok", "instagram": "Instagram", "twitter": "X"}
        return titles.get(self.extractor.strip().lower(), self.extractor.strip())
