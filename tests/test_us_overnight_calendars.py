from datetime import time
from zoneinfo import ZoneInfo

import pandas as pd

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar
from pandas_market_calendars.calendars.us_overnight import (
    OVERNIGHT_FROM,
    NASDAQExchangeCalendar,
    NYSEArcaExchangeCalendar,
)


NY = ZoneInfo("America/New_York")
ALL_TIMES = ["overnight", "pre", "market_open", "market_close", "post"]


def ny(ts: str) -> pd.Timestamp:
    return pd.Timestamp(ts, tz=NY)


def times(schedule: pd.DataFrame, columns: list[str] = ALL_TIMES, day: int = 0) -> list[str]:
    row = schedule.iloc[day]
    return [row[c].tz_convert(NY).strftime("%a %m-%d %H:%M") for c in columns]


def full_schedule(cal: NYSEExchangeCalendar, start: str, end: str) -> pd.DataFrame:
    return cal.schedule(start, end, start="overnight", end="post")


def test_registry_names_and_aliases():
    # new names resolve to the new classes
    for name, cls in [
        ("NASDAQ_23_5", NASDAQExchangeCalendar),
        ("NYSE_Arca", NYSEArcaExchangeCalendar),
        ("ARCA", NYSEArcaExchangeCalendar),
        ("ARCX", NYSEArcaExchangeCalendar),
    ]:
        assert isinstance(mcal.get_calendar(name), cls)

    # names round-trip through the registry
    assert mcal.get_calendar("NASDAQ_23_5").name == "NASDAQ_23_5"
    assert mcal.get_calendar("ARCA").name == "NYSE_Arca"

    # existing names are untouched: NASDAQ is still the NYSE calendar, which has no overnight session
    assert type(mcal.get_calendar("NASDAQ")) is NYSEExchangeCalendar
    assert mcal.get_calendar("NASDAQ").name == "NYSE"
    assert "overnight" not in mcal.get_calendar("NYSE").market_times


def test_market_times_order():
    assert NASDAQExchangeCalendar().market_times == ALL_TIMES
    assert NYSEArcaExchangeCalendar().market_times == ALL_TIMES
    assert NASDAQExchangeCalendar().open_close_map["overnight"] is True
    assert OVERNIGHT_FROM == "2026-12-07"


def test_schedule_before_start_has_zero_length_overnight():
    cal = NASDAQExchangeCalendar()

    sched = full_schedule(cal, "2026-12-04", "2026-12-04")

    assert times(sched) == [
        "Fri 12-04 04:00",
        "Fri 12-04 04:00",
        "Fri 12-04 09:30",
        "Fri 12-04 16:00",
        "Fri 12-04 20:00",
    ]
    assert sched.iloc[0]["overnight"] == pd.Timestamp("2026-12-04 09:00", tz="UTC")


def test_schedule_first_overnight_session():
    for cal in [NASDAQExchangeCalendar(), NYSEArcaExchangeCalendar()]:
        sched = full_schedule(cal, "2026-12-07", "2026-12-07")

        assert times(sched) == [
            "Sun 12-06 21:00",
            "Mon 12-07 04:00",
            "Mon 12-07 09:30",
            "Mon 12-07 16:00",
            "Mon 12-07 20:00",
        ]
        assert list(sched.iloc[0]) == [
            pd.Timestamp("2026-12-07 02:00", tz="UTC"),
            pd.Timestamp("2026-12-07 09:00", tz="UTC"),
            pd.Timestamp("2026-12-07 14:30", tz="UTC"),
            pd.Timestamp("2026-12-07 21:00", tz="UTC"),
            pd.Timestamp("2026-12-08 01:00", tz="UTC"),
        ]


def test_schedule_weeknights_and_no_friday_night():
    cal = NASDAQExchangeCalendar()

    # weeknight: Tuesday's session opens Monday evening
    sched = full_schedule(cal, "2026-12-08", "2026-12-08")
    assert times(sched, ["overnight", "pre"]) == ["Mon 12-07 21:00", "Tue 12-08 04:00"]

    # Friday is followed by Monday, whose session opens on Sunday evening, not Friday evening
    sched = full_schedule(cal, "2026-12-11", "2026-12-14")
    assert list(sched.index) == [pd.Timestamp("2026-12-11"), pd.Timestamp("2026-12-14")]
    assert times(sched, ["overnight"], day=0) == ["Thu 12-10 21:00"]
    assert times(sched, ["overnight"], day=1) == ["Sun 12-13 21:00"]


def test_schedule_thanksgiving_before_start():
    cal = NASDAQExchangeCalendar()

    sched = full_schedule(cal, "2026-11-25", "2026-11-30")

    # Thanksgiving is closed, the day after closes early, and the overnight session has not started yet
    assert pd.Timestamp("2026-11-26") not in sched.index
    assert times(sched, day=1) == [
        "Fri 11-27 04:00",
        "Fri 11-27 04:00",
        "Fri 11-27 09:30",
        "Fri 11-27 13:00",
        "Fri 11-27 17:00",
    ]
    assert (sched["overnight"] == sched["pre"]).all()


def test_schedule_christmas_and_new_year():
    cal = NASDAQExchangeCalendar()

    # Christmas Eve is a half day; its overnight session is untouched by the early close
    sched = full_schedule(cal, "2026-12-23", "2026-12-28")
    assert list(sched.index) == [pd.Timestamp("2026-12-23"), pd.Timestamp("2026-12-24"), pd.Timestamp("2026-12-28")]
    assert times(sched, day=1) == [
        "Wed 12-23 21:00",
        "Thu 12-24 04:00",
        "Thu 12-24 09:30",
        "Thu 12-24 13:00",
        "Thu 12-24 17:00",
    ]
    assert times(sched, ["overnight"], day=2) == ["Sun 12-27 21:00"]

    # New Year's Day 2027 is a Friday holiday; Monday opens on Sunday evening
    sched = full_schedule(cal, "2026-12-31", "2027-01-04")
    assert pd.Timestamp("2027-01-01") not in sched.index
    assert times(sched, ["overnight"], day=1) == ["Sun 01-03 21:00"]


def test_schedule_opens_on_the_evening_of_a_holiday():
    cal = NASDAQExchangeCalendar()

    # Martin Luther King Jr. Day is Monday 2027-01-18; Tuesday's session opens that evening
    sched = full_schedule(cal, "2027-01-15", "2027-01-19")

    assert pd.Timestamp("2027-01-18") not in sched.index
    assert times(sched, ["overnight"], day=1) == ["Mon 01-18 21:00"]


def test_schedule_daylight_saving_changeovers():
    cal = NASDAQExchangeCalendar()

    # clocks go forward on Sunday 2027-03-14: 21:00 EDT
    sched = full_schedule(cal, "2027-03-15", "2027-03-15")
    assert times(sched, ["overnight", "pre"]) == ["Sun 03-14 21:00", "Mon 03-15 04:00"]
    assert sched.iloc[0]["overnight"] == pd.Timestamp("2027-03-15 01:00", tz="UTC")
    assert sched.iloc[0]["pre"] == pd.Timestamp("2027-03-15 08:00", tz="UTC")

    # clocks go back on Sunday 2027-11-07: 21:00 EST
    sched = full_schedule(cal, "2027-11-08", "2027-11-08")
    assert times(sched, ["overnight", "pre"]) == ["Sun 11-07 21:00", "Mon 11-08 04:00"]
    assert sched.iloc[0]["overnight"] == pd.Timestamp("2027-11-08 02:00", tz="UTC")
    assert sched.iloc[0]["pre"] == pd.Timestamp("2027-11-08 09:00", tz="UTC")


def test_default_schedule_matches_nyse():
    nyse = NYSEExchangeCalendar()

    for cal in [NASDAQExchangeCalendar(), NYSEArcaExchangeCalendar()]:
        # default columns, across the start date
        pd.testing.assert_frame_equal(
            cal.schedule("2026-11-01", "2027-01-31"), nyse.schedule("2026-11-01", "2027-01-31")
        )

        # pre to post, across the start date
        pd.testing.assert_frame_equal(
            cal.schedule("2026-11-01", "2027-01-31", start="pre", end="post"),
            nyse.schedule("2026-11-01", "2027-01-31", start="pre", end="post"),
        )

        # history long before the start date, including every column
        before = cal.schedule("1990-01-01", "2026-12-04", market_times="all")
        assert (before["overnight"] == before["pre"]).all()
        pd.testing.assert_frame_equal(
            before.drop(columns="overnight"),
            nyse.schedule("1990-01-01", "2026-12-04", market_times="all"),
        )


def test_open_at_time_overnight():
    cal = NASDAQExchangeCalendar()
    sched = full_schedule(cal, "2026-12-04", "2026-12-16")

    # open during the overnight session and at its boundaries
    assert cal.open_at_time(sched, ny("2026-12-06 21:00")) is True
    assert cal.open_at_time(sched, ny("2026-12-07 22:00")) is True
    assert cal.open_at_time(sched, ny("2026-12-08 03:59")) is True
    assert cal.open_at_time(sched, ny("2026-12-08 04:00")) is True

    # closed before the first session, in the 20:00-21:00 pause, on Friday night and on the weekend
    assert cal.open_at_time(sched, ny("2026-12-06 20:59")) is False
    assert cal.open_at_time(sched, ny("2026-12-07 20:30")) is False
    assert cal.open_at_time(sched, ny("2026-12-11 21:30")) is False
    assert cal.open_at_time(sched, ny("2026-12-12 12:00")) is False

    # only_rth limits the check to market_open..market_close
    assert cal.open_at_time(sched, ny("2026-12-07 22:00"), only_rth=True) is False
    assert cal.open_at_time(sched, ny("2026-12-08 10:00"), only_rth=True) is True


def test_change_time_moves_the_start_date():
    cal = NASDAQExchangeCalendar()

    cal.change_time("overnight", ((None, time(4)), ("2027-01-25", time(21), -1)))
    sched = full_schedule(cal, "2026-12-07", "2027-01-25")

    assert times(sched, ["overnight", "pre"], day=0) == ["Mon 12-07 04:00", "Mon 12-07 04:00"]
    assert times(sched, ["overnight", "pre"], day=-1) == ["Sun 01-24 21:00", "Mon 01-25 04:00"]
    assert cal.open_close_map["overnight"] is True

    # the class default is unchanged for new instances
    assert times(full_schedule(NASDAQExchangeCalendar(), "2026-12-07", "2026-12-07"), ["overnight"]) == [
        "Sun 12-06 21:00"
    ]


def test_sources():
    nasdaq_sources = mcal.get_calendar("NASDAQ_23_5").sources
    arca_sources = mcal.get_calendar("ARCA").sources

    assert any("SR-NASDAQ-2025-109" in source.url for source in nasdaq_sources)
    assert any("SR-NYSEArca-2026-53" in source.url for source in arca_sources)
