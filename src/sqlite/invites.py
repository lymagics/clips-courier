from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.domain.invites import Invites


class SqliteInvites(Invites):
    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def add(self, token: str, deadline: int) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text(
                    "INSERT OR REPLACE INTO invites (token, deadline) "
                    "VALUES (:token, :deadline)"
                ),
                {"token": token, "deadline": deadline},
            )
            await db.commit()

    async def remove(self, token: str) -> None:
        async with AsyncSession(self.engine) as db:
            await db.execute(
                text("DELETE FROM invites WHERE token = :token"),
                {"token": token},
            )
            await db.commit()

    async def valid(self, token: str, now: int) -> bool:
        async with AsyncSession(self.engine) as db:
            rows = await db.execute(
                text(
                    "SELECT COUNT(*) FROM invites "
                    "WHERE token = :token AND deadline > :now"
                ),
                {"token": token, "now": now},
            )
            return rows.scalar_one() > 0
