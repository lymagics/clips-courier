from pathlib import Path
from typing import Any, Self

from aiogram.types import FSInputFile

from src.domain.clip import Clip
from src.domain.clips import Clips
from src.domain.downloads import Downloads
from src.domain.fault import Fault
from src.domain.friend import Friend, StoredFriend
from src.domain.friends import Friends
from src.domain.invites import Invites
from src.domain.post import Post, StoredPost
from src.domain.stat import Stat, StoredStat


class FakeUser:
    def __init__(self, id: int, username: str | None = None):
        self.id = id
        self.username = username


class FakeBot:
    def __init__(self, username: str):
        self.username = username

    async def me(self) -> FakeUser:
        return FakeUser(1, self.username)


class FakeMessage:
    def __init__(
        self,
        text: str = "",
        sender: FakeUser | None = None,
        bot: FakeBot | None = None,
    ):
        self.text = text
        self.from_user = sender
        self.bot = FakeBot("fake_bot") if bot is None else bot
        self.replies: list[str] = []
        self.videos: list[FSInputFile] = []
        self.captions: list[str] = []
        self.quoted: list[str | FSInputFile] = []

    async def answer(self, text: str):
        self.replies.append(text)

    async def answer_video(self, video: FSInputFile, caption: str = ""):
        self.videos.append(video)
        self.captions.append(caption)

    async def reply(self, text: str):
        self.replies.append(text)
        self.quoted.append(text)

    async def reply_video(self, video: FSInputFile, caption: str = ""):
        self.videos.append(video)
        self.captions.append(caption)
        self.quoted.append(video)


class FakeClip(Clip):
    def __init__(self, file: Path, caption: str = ""):
        self.origin = file
        self.note = caption

    async def file(self) -> Path:
        return self.origin

    async def post(self) -> Post:
        return StoredPost(self.origin, self.note)


class BrokenClip(Clip):
    async def file(self) -> Path:
        raise Fault("The clip is broken.")

    async def post(self) -> Post:
        raise Fault("The clip is broken.")


class FakeClips(Clips):
    def __init__(self, clip: Clip):
        self.origin = clip

    def clip(self, link: str) -> Clip:
        return self.origin


class FakeFriends(Friends):
    def __init__(self, members: dict[int, str]):
        self.members = members

    async def add(self, id: int, name: str) -> None:
        self.members[id] = name

    async def remove(self, id: int) -> None:
        del self.members[id]

    async def roster(self) -> list[Friend]:
        return [StoredFriend(id, name) for id, name in self.members.items()]


class FakeInvites(Invites):
    def __init__(self, deadlines: dict[str, int]):
        self.deadlines = deadlines

    async def add(self, token: str, deadline: int) -> None:
        self.deadlines[token] = deadline

    async def remove(self, token: str) -> None:
        del self.deadlines[token]

    async def valid(self, token: str, now: int) -> bool:
        return self.deadlines.get(token, now) > now


class FakeDownloads(Downloads):
    def __init__(self, stats: dict[str, tuple[int, int]]):
        self.stats = stats

    async def record(self, name: str, size: int) -> None:
        count, total = self.stats.get(name, (0, 0))
        self.stats[name] = (count + 1, total + size)

    async def tally(self) -> list[Stat]:
        return [
            StoredStat(name, count, size) for name, (count, size) in self.stats.items()
        ]


class FakeHandler:
    def __init__(self):
        self.events: list[Any] = []

    async def __call__(self, event: Any, data: dict[str, Any]) -> None:
        self.events.append(event)


class FakeTool:
    def __init__(self, file: Path):
        self.file = file

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *trash: object) -> bool:
        return False

    def extract_info(self, link: str) -> dict[str, Any]:
        self.file.write_bytes(b"\x00\x00\x00\x18ftypmp42-fake")
        return {"requested_downloads": [{"filepath": str(self.file)}]}


class MetaTool:
    def __init__(self, file: Path, info: dict[str, Any]):
        self.file = file
        self.info = info

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *trash: object) -> bool:
        return False

    def extract_info(self, link: str) -> dict[str, Any]:
        self.file.write_bytes(b"\x00\x00\x00\x14ftypisom-meta")
        return {"requested_downloads": [{"filepath": str(self.file)}], **self.info}


class BrokenTool:
    def __enter__(self) -> Self:
        return self

    def __exit__(self, *trash: object) -> bool:
        return False

    def extract_info(self, link: str) -> dict[str, Any]:
        raise Fault("There is no video behind the link.")
