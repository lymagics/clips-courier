from pathlib import Path
from typing import Any
from uuid import uuid4

from yt_dlp import YoutubeDL

from src.domain.clip import Clip
from src.domain.clips import Clips
from src.domain.tidy import TidyClip
from src.ytdlp.clip import YtdlpClip


class YtdlpClips(Clips):
    def __init__(self, folder: Path, options: dict[str, Any]):
        self.folder = folder
        self.options = options

    def clip(self, link: str) -> Clip:
        folder = self.folder / uuid4().hex
        options = dict(self.options)
        options["outtmpl"] = str(folder / "%(id)s.%(ext)s")
        return TidyClip(YtdlpClip(link, YoutubeDL(options)), folder)
