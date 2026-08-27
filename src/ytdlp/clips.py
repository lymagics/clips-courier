from pathlib import Path

from src.domain.clip import Clip
from src.domain.clips import Clips
from src.ytdlp.clip import YtdlpClip


class YtdlpClips(Clips):
    def __init__(self, folder: Path):
        self.folder = folder

    def clip(self, link: str) -> Clip:
        return YtdlpClip(link, self.folder)
