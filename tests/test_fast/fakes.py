from pathlib import Path
from typing import Any, Self

from aiogram.types import FSInputFile

from src.domain.clip import Clip
from src.domain.clips import Clips
from src.domain.downloads import Downloads
from src.domain.fault import Fault
from src.domain.friend import Friend, StoredFriend
from src.domain.friends import Friends
from src.domain.post import Post, StoredPost
from src.domain.stat import Stat, StoredStat


class FakeUser:
    def __init__(self, id: int, username: str | None = None):
        self.id = id
        self.username = username


class FakeMessage:
    def __init__(self, text: str = "", sender: FakeUser | None = None):
        self.text = text
        self.from_user = sender
        self.replies: list[str] = []
        self.videos: list[FSInputFile] = []
        self.captions: list[str] = []

    async def answer(self, text: str):
        self.replies.append(text)

    async def answer_video(self, video: FSInputFile, caption: str = ""):
        self.videos.append(video)
        self.captions.append(caption)


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
    def __init__(self, names: list[str]):
        self.names = names

    async def add(self, name: str) -> None:
        self.names.append(name)

    async def remove(self, name: str) -> None:
        self.names.remove(name)

    async def roster(self) -> list[Friend]:
        return [StoredFriend(name) for name in self.names]


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


class FakeRows:
    def __init__(self, rows: list[tuple[str]]):
        self.rows = rows

    def all(self) -> list[tuple[str]]:
        return self.rows


class FakeSession:
    def __init__(self):
        self.names: set[str] = set()

    async def execute(
        self, statement: Any, parameters: dict[str, str] | None = None
    ) -> FakeRows:
        query = str(statement)
        if query.startswith("INSERT"):
            self.names.add(parameters["name"])
        if query.startswith("DELETE"):
            self.names.discard(parameters["name"])
        return FakeRows([(name,) for name in sorted(self.names)])

    async def commit(self) -> None:
        pass
