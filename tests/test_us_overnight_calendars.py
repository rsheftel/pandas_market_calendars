from datetime import time
from zoneinfo import ZoneInfo

import pandas as pd

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar
from pandas_market_calendars.calendars.us_overnight import (
    NASDAQ_OVERNIGHT_CLOSE,
    OVERNIGHT_FROM,
    NASDAQExchangeCalendar,
    NYSEArcaExchangeCalendar,
)


NY = ZoneInfo("America/New_York")
ALL_TIMES = ("overnight", "pre", "market_open", "market_close", "post")
NASDAQ_TIMES = ("overnight", "overnight_close", "pre", "market_open", "market_close", "post")


def ny(ts: str) -> pd.Timestamp:
    """
    Build a New York timestamp.

    :param ts: Date and time without a timezone.
    :return: The timestamp in America/New_York.
    """
    return pd.Timestamp(ts, tz=NY)


def times(schedule: pd.DataFrame, columns: tuple[str, ...] | list[str] = ALL_TIMES, day: int = 0) -> list[str]:
    """
    Format one schedule row's times in New York time, so tests can compare readable strings.

    :param schedule: A schedule from MarketCalendar.schedule.
    :param columns: The market time columns to format, in order.
    :param day: Position of the row in the schedule.
    :return: Each time as "Day MM-DD HH:MM".
    """
    row = schedule.iloc[day]
    return [row[column].tz_convert(NY).strftime("%a %m-%d %H:%M") for column in columns]


def full_schedule(cal: NYSEExchangeCalendar, start: str, end: str) -> pd.DataFrame:
    """
    Build a schedule with every column from overnight to post.

    :param cal: The calendar to schedule.
    :param start: First date of the schedule.
    :param end: Last date of the schedule.
    :return: The schedule with overnight through post columns, including overnight_close on Nasdaq.
    """
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
    assert NASDAQExchangeCalendar().market_times == list(NASDAQ_TIMES)
    assert NYSEArcaExchangeCalendar().market_times == list(ALL_TIMES)
    assert "overnight_close" not in NYSEArcaExchangeCalendar().market_times
    assert NASDAQExchangeCalendar().open_close_map["overnight"] is True
    assert NASDAQExchangeCalendar().open_close_map["overnight_close"] is False
    assert OVERNIGHT_FROM == "2026-12-07"
    assert time(3, 55) == NASDAQ_OVERNIGHT_CLOSE


def test_schedule_before_start_has_zero_length_overnight():
    cal = NASDAQExchangeCalendar()

    sched = full_schedule(cal, "2026-12-04", "2026-12-04")

    assert times(sched, NASDAQ_TIMES) == [
        "Fri 12-04 04:00",
        "Fri 12-04 04:00",
        "Fri 12-04 04:00",
        "Fri 12-04 09:30",
        "Fri 12-04 16:00",
        "Fri 12-04 20:00",
    ]
    assert sched.iloc[0]["overnight"] == pd.Timestamp("2026-12-04 09:00", tz="UTC")
    assert sched.iloc[0]["overnight_close"] == sched.iloc[0]["pre"]


def test_schedule_first_overnight_session():
    nasdaq = full_schedule(NASDAQExchangeCalendar(), "2026-12-07", "2026-12-07")
    assert times(nasdaq, NASDAQ_TIMES) == [
        "Sun 12-06 21:00",
        "Mon 12-07 03:55",
        "Mon 12-07 04:00",
        "Mon 12-07 09:30",
        "Mon 12-07 16:00",
        "Mon 12-07 20:00",
    ]
    assert list(nasdaq.iloc[0]) == [
        pd.Timestamp("2026-12-07 02:00", tz="UTC"),
        pd.Timestamp("2026-12-07 08:55", tz="UTC"),
        pd.Timestamp("2026-12-07 09:00", tz="UTC"),
        pd.Timestamp("2026-12-07 14:30", tz="UTC"),
        pd.Timestamp("2026-12-07 21:00", tz="UTC"),
        pd.Timestamp("2026-12-08 01:00", tz="UTC"),
    ]

    arca = full_schedule(NYSEArcaExchangeCalendar(), "2026-12-07", "2026-12-07")
    assert times(arca) == [
        "Sun 12-06 21:00",
        "Mon 12-07 04:00",
        "Mon 12-07 09:30",
        "Mon 12-07 16:00",
        "Mon 12-07 20:00",
    ]
    assert list(arca.iloc[0]) == [
        pd.Timestamp("2026-12-07 02:00", tz="UTC"),
        pd.Timestamp("2026-12-07 09:00", tz="UTC"),
        pd.Timestamp("2026-12-07 14:30", tz="UTC"),
        pd.Timestamp("2026-12-07 21:00", tz="UTC"),
        pd.Timestamp("2026-12-08 01:00", tz="UTC"),
    ]


def test_schedule_weeknights_and_no_friday_night():
    cal = NASDAQExchangeCalendar()

    # weeknight: Tuesday's session opens Monday evening and ends at 03:55
    sched = full_schedule(cal, "2026-12-08", "2026-12-08")
    assert times(sched, ["overnight", "overnight_close", "pre"]) == [
        "Mon 12-07 21:00",
        "Tue 12-08 03:55",
        "Tue 12-08 04:00",
    ]

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
    assert times(sched, NASDAQ_TIMES, day=1) == [
        "Fri 11-27 04:00",
        "Fri 11-27 04:00",
        "Fri 11-27 04:00",
        "Fri 11-27 09:30",
        "Fri 11-27 13:00",
        "Fri 11-27 17:00",
    ]
    assert (sched["overnight"] == sched["pre"]).all()
    assert (sched["overnight_close"] == sched["pre"]).all()


def test_schedule_christmas_and_new_year():
    cal = NASDAQExchangeCalendar()

    # Christmas Eve is a half day; its overnight session is untouched by the early close and still ends at 03:55
    sched = full_schedule(cal, "2026-12-23", "2026-12-28")
    assert list(sched.index) == [pd.Timestamp("2026-12-23"), pd.Timestamp("2026-12-24"), pd.Timestamp("2026-12-28")]
    assert times(sched, NASDAQ_TIMES, day=1) == [
        "Wed 12-23 21:00",
        "Thu 12-24 03:55",
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


def test_schedule_half_day_before_a_midweek_holiday():
    cal = NASDAQExchangeCalendar()

    # Monday 2029-12-24 closes early and Tuesday is Christmas; Wednesday's session opens on Christmas evening
    sched = full_schedule(cal, "2029-12-24", "2029-12-26")

    assert list(sched.index) == [pd.Timestamp("2029-12-24"), pd.Timestamp("2029-12-26")]
    assert times(sched, NASDAQ_TIMES, day=0) == [
        "Sun 12-23 21:00",
        "Mon 12-24 03:55",
        "Mon 12-24 04:00",
        "Mon 12-24 09:30",
        "Mon 12-24 13:00",
        "Mon 12-24 17:00",
    ]
    assert times(sched, ["overnight", "pre"], day=1) == ["Tue 12-25 21:00", "Wed 12-26 04:00"]


def test_schedule_opens_on_the_evening_of_a_holiday():
    for cal in [NASDAQExchangeCalendar(), NYSEArcaExchangeCalendar()]:
        # Martin Luther King Jr. Day is Monday 2027-01-18; Tuesday's session opens that evening
        sched = full_schedule(cal, "2027-01-15", "2027-01-19")

        assert pd.Timestamp("2027-01-18") not in sched.index
        assert times(sched, ["overnight"], day=1) == ["Mon 01-18 21:00"]


def test_schedule_daylight_saving_changeovers():
    cal = NASDAQExchangeCalendar()

    # clocks go forward on Sunday 2027-03-14: 21:00 EDT, close at 03:55 EDT
    sched = full_schedule(cal, "2027-03-15", "2027-03-15")
    assert times(sched, ["overnight", "overnight_close", "pre"]) == [
        "Sun 03-14 21:00",
        "Mon 03-15 03:55",
        "Mon 03-15 04:00",
    ]
    assert sched.iloc[0]["overnight"] == pd.Timestamp("2027-03-15 01:00", tz="UTC")
    assert sched.iloc[0]["overnight_close"] == pd.Timestamp("2027-03-15 07:55", tz="UTC")
    assert sched.iloc[0]["pre"] == pd.Timestamp("2027-03-15 08:00", tz="UTC")

    # clocks go back on Sunday 2027-11-07: 21:00 EST, close at 03:55 EST
    sched = full_schedule(cal, "2027-11-08", "2027-11-08")
    assert times(sched, ["overnight", "overnight_close", "pre"]) == [
        "Sun 11-07 21:00",
        "Mon 11-08 03:55",
        "Mon 11-08 04:00",
    ]
    assert sched.iloc[0]["overnight"] == pd.Timestamp("2027-11-08 02:00", tz="UTC")
    assert sched.iloc[0]["overnight_close"] == pd.Timestamp("2027-11-08 08:55", tz="UTC")
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
        extra = [column for column in ("overnight", "overnight_close") if column in before.columns]
        if "overnight_close" in before.columns:
            assert (before["overnight_close"] == before["pre"]).all()
        pd.testing.assert_frame_equal(
            before.drop(columns=extra),
            nyse.schedule("1990-01-01", "2026-12-04", market_times="all"),
        )


def test_open_at_time_overnight():
    cal = NASDAQExchangeCalendar()
    sched = full_schedule(cal, "2026-12-04", "2026-12-16")

    # open during the overnight session and at its start
    assert cal.open_at_time(sched, ny("2026-12-06 21:00")) is True
    assert cal.open_at_time(sched, ny("2026-12-07 22:00")) is True
    assert cal.open_at_time(sched, ny("2026-12-08 03:54")) is True
    # Nasdaq's Night Session ends at 03:55, then a five-minute pause until pre at 04:00
    assert cal.open_at_time(sched, ny("2026-12-08 03:55")) is False
    assert cal.open_at_time(sched, ny("2026-12-08 03:59")) is False
    assert cal.open_at_time(sched, ny("2026-12-08 04:00")) is True

    # closed before the first session, in the 20:00-21:00 pause, on Friday night and on the weekend
    assert cal.open_at_time(sched, ny("2026-12-06 20:59")) is False
    assert cal.open_at_time(sched, ny("2026-12-07 20:30")) is False
    assert cal.open_at_time(sched, ny("2026-12-11 21:30")) is False
    assert cal.open_at_time(sched, ny("2026-12-12 12:00")) is False

    # only_rth limits the check to market_open..market_close
    assert cal.open_at_time(sched, ny("2026-12-07 22:00"), only_rth=True) is False
    assert cal.open_at_time(sched, ny("2026-12-08 10:00"), only_rth=True) is True

    # Arca has no 03:55 close; the overnight session runs into pre at 04:00
    arca = NYSEArcaExchangeCalendar()
    arca_sched = full_schedule(arca, "2026-12-04", "2026-12-16")
    assert arca.open_at_time(arca_sched, ny("2026-12-08 03:57")) is True


def test_change_time_moves_the_start_date():
    cal = NASDAQExchangeCalendar()

    # the industry fallback launch is Sunday 2027-01-24, so trading date 2027-01-25 is the first with a session
    cal.change_time("overnight", ((None, time(4)), ("2027-01-25", time(21), -1)))
    cal.change_time("overnight_close", ((None, time(4)), ("2027-01-25", time(3, 55))))
    sched = full_schedule(cal, "2026-12-07", "2027-01-25")

    assert times(sched, ["overnight", "overnight_close", "pre"], day=0) == [
        "Mon 12-07 04:00",
        "Mon 12-07 04:00",
        "Mon 12-07 04:00",
    ]
    assert times(sched, ["overnight", "overnight_close", "pre"], day=-1) == [
        "Sun 01-24 21:00",
        "Mon 01-25 03:55",
        "Mon 01-25 04:00",
    ]
    assert cal.open_close_map["overnight"] is True
    assert cal.open_close_map["overnight_close"] is False

    # the class default is unchanged for new instances
    assert times(
        full_schedule(NASDAQExchangeCalendar(), "2026-12-07", "2026-12-07"), ["overnight", "overnight_close"]
    ) == [
        "Sun 12-06 21:00",
        "Mon 12-07 03:55",
    ]


def test_sources():
    nasdaq_sources = mcal.get_calendar("NASDAQ_23_5").sources
    arca_sources = mcal.get_calendar("ARCA").sources

    assert any("SR-NASDAQ-2025-109" in source.name for source in nasdaq_sources)
    assert any("2026-72" in source.name for source in nasdaq_sources)
    assert any("SR-NYSEArca-2026-53" in source.name for source in arca_sources)


def test_open_at_time_needs_the_next_trading_date_row():
    cal = NASDAQExchangeCalendar()

    # Sunday evening belongs to Monday's row: a schedule for Sunday alone is empty
    assert full_schedule(cal, "2026-12-06", "2026-12-06").empty

    # a schedule from today through the next trading day covers it
    sched = full_schedule(cal, "2026-12-06", "2026-12-07")
    assert cal.open_at_time(sched, ny("2026-12-06 22:00")) is True

    # Monday 22:00 belongs to Tuesday's row
    sched = full_schedule(cal, "2026-12-07", "2026-12-08")
    assert cal.open_at_time(sched, ny("2026-12-07 22:00")) is True
    assert cal.open_at_time(sched, ny("2026-12-07 20:30")) is False


def test_schedule_late_open_keeps_overnight_without_forced_special_times():
    cal = NASDAQExchangeCalendar()
    # move the start back so an existing NYSE late open (2001-09-17, 09:33) falls inside the session's range
    cal.change_time("overnight", ((None, time(4)), ("2001-01-01", time(21), -1)))
    cal.change_time("overnight_close", ((None, time(4)), ("2001-01-01", time(3, 55))))

    forced = full_schedule(cal, "2001-09-17", "2001-09-17")
    kept = cal.schedule("2001-09-17", "2001-09-17", start="overnight", end="post", force_special_times=False)

    # the default clamps every column before the late open, overnight and pre alike
    assert times(forced, ["overnight", "pre", "market_open"]) == [
        "Mon 09-17 09:33",
        "Mon 09-17 09:33",
        "Mon 09-17 09:33",
    ]
    # force_special_times=False keeps the overnight time
    assert times(kept, ["overnight", "overnight_close", "market_open"]) == [
        "Sun 09-16 21:00",
        "Mon 09-17 03:55",
        "Mon 09-17 09:33",
    ]
