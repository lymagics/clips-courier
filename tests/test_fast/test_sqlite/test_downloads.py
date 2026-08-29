import shutil
import sqlite3
from pathlib import Path

from hamcrest import assert_that, has_item, has_length, is_
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import NullPool

from src.sqlite.downloads import SqliteDownloads
from tests.test_fast.schema import MigratedSchema


async def test_lists_recorded_download():
    folder = Path("tmp/test-downloads-record")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "courier.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/courier.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(AsyncSession(engine))
    await downloads.record("amber_heron", 2048)
    assert_that(
        [stat.name() for stat in await downloads.tally()],
        has_item("amber_heron"),
        "The sqlite downloads must list a recorded download",
    )


async def test_counts_repeated_downloads_of_one_user():
    folder = Path("tmp/test-downloads-count")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "wire.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/wire.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(AsyncSession(engine))
    await downloads.record("teal_badger", 100)
    await downloads.record("teal_badger", 300)
    await downloads.record("teal_badger", 555)
    assert_that(
        [stat.count() for stat in await downloads.tally()],
        has_item(3),
        "The sqlite downloads must count repeated downloads of one user",
    )


async def test_sums_data_size_per_user():
    folder = Path("tmp/test-downloads-sum")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "sum.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/sum.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(AsyncSession(engine))
    await downloads.record("olive_stoat", 4001)
    await downloads.record("olive_stoat", 999)
    assert_that(
        [stat.size() for stat in await downloads.tally()],
        has_item(5000),
        "The sqlite downloads must sum the data size per user",
    )


async def test_builds_empty_tally_from_fresh_database():
    folder = Path("tmp/test-downloads-empty")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "blank.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/blank.db", poolclass=NullPool
    )
    assert_that(
        await SqliteDownloads(AsyncSession(engine)).tally(),
        has_length(0),
        "The sqlite downloads must build an empty tally from a fresh database",
    )


async def test_keeps_tally_for_new_session_over_same_file():
    folder = Path("tmp/test-downloads-restart")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "keep.db").upgrade()
    first = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/keep.db", poolclass=NullPool
    )
    await SqliteDownloads(AsyncSession(first)).record("dusty_falcon", 7331)
    await first.dispose()
    second = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/keep.db", poolclass=NullPool
    )
    assert_that(
        [stat.size() for stat in await SqliteDownloads(AsyncSession(second)).tally()],
        has_item(7331),
        "The sqlite downloads must keep the tally for a new session over one file",
    )


async def test_stores_separate_row_for_every_download():
    folder = Path("tmp/test-downloads-rows")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "rows.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/rows.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(AsyncSession(engine))
    await downloads.record("gilded_heron", 640)
    await downloads.record("gilded_heron", 1919)
    await engine.dispose()
    ledger = sqlite3.connect(folder / "rows.db")
    rows = ledger.execute("SELECT name FROM downloads").fetchall()
    ledger.close()
    assert_that(
        rows,
        has_length(2),
        "The sqlite downloads must store a separate row for every download",
    )


async def test_orders_tally_by_download_count_descending():
    folder = Path("tmp/test-downloads-order")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "rank.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/rank.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(AsyncSession(engine))
    await downloads.record("shy_viper", 11)
    await downloads.record("bold_otter", 22)
    await downloads.record("bold_otter", 33)
    assert_that(
        (await downloads.tally())[0].name(),
        is_("bold_otter"),
        "The sqlite downloads must order the tally by download count, descending",
    )
