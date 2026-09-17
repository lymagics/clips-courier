from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.domain.friend import Friend, StoredFriend
from src.domain.friends import Friends


class SqliteFriends(Friends):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def add(self, id: int, name: str) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text("INSERT OR REPLACE INTO friends (id, name) VALUES (:id, :name)"),
                {"id": id, "name": name},
            )
            await db.commit()

    async def remove(self, id: int) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text("DELETE FROM friends WHERE id = :id"),
                {"id": id},
            )
            await db.commit()

    async def roster(self) -> list[Friend]:
        async with AsyncSession(self.engine) as db:
            rows = await db.execute(
                text("SELECT id, name FROM friends ORDER BY name, id")
            )
            return [StoredFriend(row[0], row[1]) for row in rows.all()]
