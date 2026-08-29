import logging
from os import environ
from pathlib import Path
from tempfile import gettempdir

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from src.bot import Bot
from src.commands.download import DownloadCommand
from src.commands.friend import FriendCommand
from src.commands.friends import FriendsCommand
from src.commands.help import HelpCommand
from src.commands.owned import OwnedCommand
from src.commands.removal import RemovalCommand
from src.commands.start import StartCommand
from src.commands.stats import StatsCommand
from src.commands.trusted import TrustedCommand
from src.sqlite.downloads import SqliteDownloads
from src.sqlite.friends import SqliteFriends
from src.ytdlp.clips import YtdlpClips

load_dotenv()

owner = int(environ["OWNER_ID"])
engine = create_async_engine(
    "sqlite+aiosqlite:///" + environ.get("DB_PATH", "courier.db")
)
friends = SqliteFriends(AsyncSession(engine))
downloads = SqliteDownloads(AsyncSession(engine))
clips = YtdlpClips(
    Path(gettempdir()),
    {
        "quiet": True,
        "no_warnings": True,
        "noprogress": True,
        "retries": 3,
        "socket_timeout": 30,
        "logger": logging.getLogger("yt_dlp"),
    },
)

dispatcher = Bot(
    StartCommand(environ.get("BOT_NAME", "")),
    HelpCommand(environ.get("BOT_NAME", ""), owner),
    TrustedCommand(DownloadCommand(clips, downloads), owner, friends),
    OwnedCommand(FriendCommand(friends), owner),
    OwnedCommand(FriendsCommand(friends), owner),
    OwnedCommand(RemovalCommand(friends), owner),
    OwnedCommand(StatsCommand(downloads), owner),
).bot(environ["BOT_KEY"])

if __name__ == "__main__":
    dispatcher.run_polling(dispatcher["courier"])
