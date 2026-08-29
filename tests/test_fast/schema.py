import asyncio
from pathlib import Path

from alembic import command
from alembic.config import Config


class MigratedSchema:
    def __init__(self, path: Path):
        self.path = path

    async def upgrade(self) -> None:
        await asyncio.to_thread(self._apply)

    def _apply(self) -> None:
        config = Config(Path(__file__).resolve().parents[2] / "alembic.ini")
        config.set_main_option("sqlalchemy.url", f"sqlite+aiosqlite:///{self.path}")
        command.upgrade(config, "head")
