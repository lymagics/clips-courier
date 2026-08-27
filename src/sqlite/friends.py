from pathlib import Path

import aiosqlite

from src.domain.friend import Friend, StoredFriend
from src.domain.friends import Friends


class SqliteFriends(Friends):
    def __init__(self, path: Path):
        self.path = path

    async def add(self, name: str) -> None:
        async with aiosqlite.connect(self.path) as db:
            await self._prepare(db)
            await db.execute("INSERT OR IGNORE INTO friends (name) VALUES (?)", (name,))
            await db.commit()

    async def remove(self, name: str) -> None:
        async with aiosqlite.connect(self.path) as db:
            await self._prepare(db)
            await db.execute("DELETE FROM friends WHERE name = ?", (name,))
            await db.commit()

    async def roster(self) -> list[Friend]:
        async with aiosqlite.connect(self.path) as db:
            await self._prepare(db)
            rows = await db.execute_fetchall("SELECT name FROM friends ORDER BY name")
        return [StoredFriend(row[0]) for row in rows]

    async def _prepare(self, db: aiosqlite.Connection) -> None:
        await db.execute("CREATE TABLE IF NOT EXISTS friends (name TEXT PRIMARY KEY)")
