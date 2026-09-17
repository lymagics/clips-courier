import shutil
from pathlib import Path

from hamcrest import assert_that, is_
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from src.sqlite.invites import SqliteInvites
from tests.test_fast.schema import MigratedSchema


async def test_accepts_token_before_deadline():
    folder = Path("tmp/test-invites-fresh")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "courier.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/courier.db", poolclass=NullPool
    )
    invites = SqliteInvites(engine)
    await invites.add("Qw3-rTy_u", 4102444800)
    assert_that(
        await invites.valid("Qw3-rTy_u", 1800000000),
        is_(True),
        "The sqlite invites must accept a token before its deadline",
    )


async def test_rejects_token_at_deadline():
    folder = Path("tmp/test-invites-deadline")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "late.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/late.db", poolclass=NullPool
    )
    invites = SqliteInvites(engine)
    await invites.add("z9_late", 1500000000)
    assert_that(
        await invites.valid("z9_late", 1500000000),
        is_(False),
        "The sqlite invites must reject a token at its deadline",
    )


async def test_rejects_unknown_token():
    folder = Path("tmp/test-invites-unknown")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "none.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/none.db", poolclass=NullPool
    )
    assert_that(
        await SqliteInvites(engine).valid("never-minted", 1700000000),
        is_(False),
        "The sqlite invites must reject a token that was never minted",
    )


async def test_rejects_removed_token():
    folder = Path("tmp/test-invites-removed")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "spent.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/spent.db", poolclass=NullPool
    )
    invites = SqliteInvites(engine)
    await invites.add("one-shot_42", 4102444800)
    await invites.remove("one-shot_42")
    assert_that(
        await invites.valid("one-shot_42", 1900000000),
        is_(False),
        "The sqlite invites must reject a removed token",
    )
