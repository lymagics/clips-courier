import shutil
from pathlib import Path

from src.domain.clip import Clip
from src.domain.post import Post


class TidyClip(Clip):
    def __init__(self, clip: Clip, folder: Path):
        self.origin = clip
        self.folder = folder

    async def file(self) -> Path:
        return (await self.post()).file()

    async def post(self) -> Post:
        try:
            return await self.origin.post()
        except Exception:
            shutil.rmtree(self.folder, ignore_errors=True)
            raise
