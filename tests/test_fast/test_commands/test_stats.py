from aiogram import Router
from hamcrest import assert_that, contains_string, instance_of

from src.commands.owned import OwnedCommand
from src.commands.stats import StatsCommand
from tests.test_fast.fakes import FakeDownloads, FakeHandler, FakeMessage, FakeUser


async def test_shows_line_per_user():
    message = FakeMessage("/st", FakeUser(9155))
    await StatsCommand(
        FakeDownloads({"lilac_crow": (6, 4096), "mossy_boar": (1, 512)})
    ).answer(message)
    assert_that(
        message.replies[0],
        contains_string("mossy_boar"),
        "The stats command must show a line for every user",
    )


async def test_shows_download_count_of_user():
    message = FakeMessage("/st", FakeUser(3378))
    await StatsCommand(FakeDownloads({"sable_lynx": (41, 1024)})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("41"),
        "The stats command must show the download count of a user",
    )


async def test_shows_data_volume_in_human_readable_unit():
    message = FakeMessage("/st", FakeUser(6410))
    await StatsCommand(FakeDownloads({"ashen_tern": (2, 3145728)})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("3.0 MB"),
        "The stats command must show the data volume in a human-readable unit",
    )


async def test_answers_friendly_note_when_nothing_recorded():
    message = FakeMessage("/st", FakeUser(1287))
    await StatsCommand(FakeDownloads({})).answer(message)
    assert_that(
        message.replies[0],
        contains_string("No downloads yet"),
        "The stats command must answer with a friendly note when nothing is recorded",
    )


async def test_refuses_stranger_behind_owner_guard():
    message = FakeMessage("/st", FakeUser(74747))
    await OwnedCommand(StatsCommand(FakeDownloads({})), 52001).guard(
        FakeHandler(), message, {}
    )
    assert_that(
        message.replies[0],
        contains_string("owner"),
        "The stats command behind the owner guard must refuse a stranger",
    )


def test_builds_aiogram_router():
    assert_that(
        StatsCommand(FakeDownloads({})).router(),
        instance_of(Router),
        "The stats command must build an aiogram router",
    )
