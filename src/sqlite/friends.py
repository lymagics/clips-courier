from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.domain.friend import Friend, StoredFriend
from src.domain.friends import Friends


class SqliteFriends(Friends):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def add(self, name: str) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text("INSERT OR IGNORE INTO friends (name) VALUES (:name)"),
                {"name": name},
            )
            await db.commit()

    async def remove(self, name: str) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text("DELETE FROM friends WHERE name = :name"),
                {"name": name},
            )
            await db.commit()

    async def roster(self) -> list[Friend]:
        async with AsyncSession(self.engine) as db:
            rows = await db.execute(text("SELECT name FROM friends ORDER BY name"))
            return [StoredFriend(row[0]) for row in rows.all()]
