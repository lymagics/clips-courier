import asyncio
import json
from pathlib import Path
from typing import Any

from src.domain.account import Account
from src.domain.caption import Caption
from src.domain.clip import Clip
from src.domain.fault import Fault
from src.domain.platform import Platform
from src.domain.post import Post, StoredPost
from src.gallery.gallery import Gallery


class GalleryClip(Clip):
    def __init__(self, link: str, folder: Path, gallery: Gallery):
        self.link = link
        self.folder = folder
        self.gallery = gallery

    async def post(self) -> Post:
        try:
            return await asyncio.to_thread(self._post)
        except Exception as e:
            raise Fault("The post cannot be downloaded.") from e

    def _post(self) -> Post:
        self.gallery.fetch(self.link, self.folder)
        files = sorted(file for file in self.folder.iterdir() if file.suffix != ".json")
        if not files:
            raise Fault("The link holds no media.")
        return StoredPost(files, self._caption(files[0]))

    def _caption(self, file: Path) -> str:
        meta = json.loads(
            file.with_name(file.name + ".json").read_text(encoding="utf-8")
        )
        author = meta.get("author") or {}
        return Caption(
            self._first(meta, "content", "description", "title"),
            Account(
                self._first(author, "name", "uniqueId")
                or self._first(meta, "username", "user"),
                self._first(author, "nick", "nickname")
                or self._first(meta, "fullname"),
            ).text(),
            Platform(self._first(meta, "category")).text(),
        ).text()

    def _first(self, source: dict[str, Any], *keys: str) -> str:
        return next(
            (
                str(source[key])
                for key in keys
                if isinstance(source.get(key), str) and source[key]
            ),
            "",
        )
