from pathlib import Path

from aiogram.types import Message

from src.domain.media import Media
from src.telegram.album import Album
from src.telegram.attachment import Attachment
from src.telegram.photo import Photo
from src.telegram.video import Video


class Parcel(Attachment):
    def __init__(self, files: list[Path], caption: str):
        self.files = files
        self.caption = caption

    async def send(self, message: Message) -> None:
        await self._attachment().send(message)

    def _attachment(self) -> Attachment:
        return (
            Album(self.files, self.caption)
            if len(self.files) > 1
            else (
                Photo(self.files[0], self.caption)
                if Media(self.files[0]).pictorial()
                else Video(self.files[0], self.caption)
            )
        )
