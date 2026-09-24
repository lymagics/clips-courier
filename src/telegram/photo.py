from pathlib import Path

from aiogram.types import FSInputFile, Message

from src.telegram.attachment import Attachment


class Photo(Attachment):
    def __init__(self, file: Path, caption: str):
        self.file = file
        self.caption = caption

    async def send(self, message: Message) -> None:
        await message.reply_photo(FSInputFile(self.file), caption=self.caption or None)
