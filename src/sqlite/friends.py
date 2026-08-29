from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.friend import Friend, StoredFriend
from src.domain.friends import Friends


class SqliteFriends(Friends):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add(self, name: str) -> None:
        await self.db.execute(
            text("INSERT OR IGNORE INTO friends (name) VALUES (:name)"),
            {"name": name},
        )
        await self.db.commit()

    async def remove(self, name: str) -> None:
        await self.db.execute(
            text("DELETE FROM friends WHERE name = :name"),
            {"name": name},
        )
        await self.db.commit()

    async def roster(self) -> list[Friend]:
        rows = await self.db.execute(text("SELECT name FROM friends ORDER BY name"))
        await self.db.commit()
        return [StoredFriend(row[0]) for row in rows.all()]
