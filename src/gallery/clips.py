from pathlib import Path
from uuid import uuid4

from src.domain.clip import Clip
from src.domain.clips import Clips
from src.domain.tidy import TidyClip
from src.gallery.clip import GalleryClip
from src.gallery.gallery import Gallery


class GalleryClips(Clips):
    def __init__(self, folder: Path, gallery: Gallery):
        self.folder = folder
        self.gallery = gallery

    def clip(self, link: str) -> Clip:
        folder = self.folder / uuid4().hex
        return TidyClip(GalleryClip(link, folder, self.gallery), folder)
