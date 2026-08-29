from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.downloads import Downloads
from src.domain.stat import Stat, StoredStat


class SqliteDownloads(Downloads):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def record(self, name: str, size: int) -> None:
        await self.db.execute(
            text("INSERT INTO downloads (name, size) VALUES (:name, :size)"),
            {"name": name, "size": size},
        )
        await self.db.commit()

    async def tally(self) -> list[Stat]:
        rows = await self.db.execute(
            text(
                "SELECT name, COUNT(*), SUM(size) FROM downloads "
                "GROUP BY name ORDER BY COUNT(*) DESC, name"
            )
        )
        await self.db.commit()
        return [StoredStat(row[0], row[1], row[2]) for row in rows.all()]
