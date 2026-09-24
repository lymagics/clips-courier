from src.domain.clip import Clip
from src.domain.clips import Clips
from src.domain.fallback import FallbackClip


class FallbackClips(Clips):
    def __init__(self, first: Clips, second: Clips):
        self.first = first
        self.second = second

    def clip(self, link: str) -> Clip:
        return FallbackClip(self.first.clip(link), self.second.clip(link))
