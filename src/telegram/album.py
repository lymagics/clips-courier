from itertools import pairwise
from pathlib import Path

from aiogram.types import FSInputFile, InputMediaPhoto, InputMediaVideo, Message

from src.domain.media import Media
from src.telegram.attachment import Attachment


class Album(Attachment):
    def __init__(self, files: list[Path], caption: str):
        self.files = files
        self.caption = caption

    async def send(self, message: Message) -> None:
        for start, end in pairwise(self._edges()):
            await message.reply_media_group(
                [
                    self._item(file, self.caption if index == 0 else "")
                    for index, file in enumerate(self.files[start:end], start)
                ]
            )

    def _edges(self) -> list[int]:
        edges = [*range(0, len(self.files), 10), len(self.files)]
        if len(edges) > 2 and edges[-1] - edges[-2] == 1:
            edges[-2] -= 1
        return edges

    def _item(self, file: Path, caption: str) -> InputMediaPhoto | InputMediaVideo:
        kind = InputMediaPhoto if Media(file).pictorial() else InputMediaVideo
        return kind(media=FSInputFile(file), caption=caption or None)
