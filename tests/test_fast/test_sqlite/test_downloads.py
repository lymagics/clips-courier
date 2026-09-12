import asyncio
import shutil
import sqlite3
from pathlib import Path

import pytest
from hamcrest import assert_that, has_item, has_length, is_
from sqlalchemy.ext.asyncio import create_async_engine
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
    downloads = SqliteDownloads(engine)
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
    downloads = SqliteDownloads(engine)
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
    downloads = SqliteDownloads(engine)
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
        await SqliteDownloads(engine).tally(),
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
    await SqliteDownloads(first).record("dusty_falcon", 7331)
    await first.dispose()
    second = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/keep.db", poolclass=NullPool
    )
    assert_that(
        [stat.size() for stat in await SqliteDownloads(second).tally()],
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
    downloads = SqliteDownloads(engine)
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
    downloads = SqliteDownloads(engine)
    await downloads.record("shy_viper", 11)
    await downloads.record("bold_otter", 22)
    await downloads.record("bold_otter", 33)
    assert_that(
        (await downloads.tally())[0].name(),
        is_("bold_otter"),
        "The sqlite downloads must order the tally by download count, descending",
    )


async def test_records_downloads_from_concurrent_tasks():
    folder = Path("tmp/test-downloads-concurrent")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "race.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/race.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(engine)
    await asyncio.gather(
        downloads.record("hasty_mole", 13),
        downloads.record("hasty_mole", 17),
        downloads.record("hasty_mole", 19),
        downloads.record("hasty_mole", 23),
        downloads.record("hasty_mole", 29),
    )
    assert_that(
        [stat.count() for stat in await downloads.tally()],
        has_item(5),
        "The sqlite downloads must record downloads from concurrent tasks",
    )


@pytest.mark.skip(reason="Reproduces #37, unskip once fixed")
async def test_merges_downloads_of_one_user_across_username_casing():
    folder = Path("tmp/test-downloads-casing")
    shutil.rmtree(folder, ignore_errors=True)
    folder.mkdir(parents=True)
    await MigratedSchema(folder / "case.db").upgrade()
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{folder}/case.db", poolclass=NullPool
    )
    downloads = SqliteDownloads(engine)
    await downloads.record("MossyLynx_7", 512)
    await downloads.record("mossylynx_7", 4096)
    assert_that(
        await downloads.tally(),
        has_length(1),
        "The sqlite downloads must merge one user's downloads across username casing",
    )
