from src.domain.clip import Clip
from src.domain.clips import Clips
from src.domain.plain import PlainClip


class PlainClips(Clips):
    def __init__(self, clips: Clips):
        self.origin = clips

    def clip(self, link: str) -> Clip:
        return PlainClip(self.origin.clip(link))
