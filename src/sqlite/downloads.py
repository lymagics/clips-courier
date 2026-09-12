from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.domain.downloads import Downloads
from src.domain.stat import Stat, StoredStat


class SqliteDownloads(Downloads):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def record(self, name: str, size: int) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text("INSERT INTO downloads (name, size) VALUES (:name, :size)"),
                {"name": name, "size": size},
            )
            await db.commit()

    async def tally(self) -> list[Stat]:
        async with AsyncSession(self.engine) as db:
            rows = await db.execute(
                text(
                    "SELECT name, COUNT(*), SUM(size) FROM downloads "
                    "GROUP BY name ORDER BY COUNT(*) DESC, name"
                )
            )
            return [StoredStat(row[0], row[1], row[2]) for row in rows.all()]
