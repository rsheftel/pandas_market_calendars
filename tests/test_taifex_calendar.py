from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.taifex import TAIFEXDayCalendar, TAIFEXExchangeCalendar


TPE = ZoneInfo("Asia/Taipei")
ALL_TIMES = ("market_open", "night_close", "day_open", "market_close")

# Exceptions to a Monday-Friday week in TAIFEX's daily TX (TAIEX futures) data from 2002-01-01 to 2026-11-26
# (https://www.taifex.com.tw/cht/3/dlFutDailyMarketView): weekdays without trading ("closed"), Saturday sessions
# ("saturday_session"), and trading days since the after-hours launch that had no after-hours session
# ("no_after_hours"). Every other weekday in the range is a trading day.
SESSION_EXCEPTIONS = Path(__file__).parent / "data" / "taifex_tx_session_exceptions.csv"
FIRST_DAY, LAST_DAY = "2002-01-01", "2026-11-26"


def session_exceptions(kind: str) -> pd.DatetimeIndex:
    """
    Read one kind of date from the TAIFEX session exceptions file.

    :param kind: "closed", "saturday_session" or "no_after_hours".
    :return: The dates of that kind.
    """
    data = pd.read_csv(SESSION_EXCEPTIONS, parse_dates=["date"])
    return pd.DatetimeIndex(data.loc[data["kind"] == kind, "date"])


def tpe(ts: str) -> pd.Timestamp:
    """
    Build a Taipei timestamp.

    :param ts: Date and time without a timezone.
    :return: The timestamp in Asia/Taipei.
    """
    return pd.Timestamp(ts, tz=TPE)


def times(schedule: pd.DataFrame, day: str, columns: tuple[str, ...] = ALL_TIMES) -> list[str]:
    """
    Format one schedule row's times in Taipei time, so tests can compare readable strings.

    :param schedule: A schedule from MarketCalendar.schedule.
    :param day: Trading day of the row.
    :param columns: The market time columns to format, in order.
    :return: Each time as "Day MM-DD HH:MM".
    """
    row = schedule.loc[day]
    return [row[column].tz_convert(TPE).strftime("%a %m-%d %H:%M") for column in columns]


def test_registry_names_and_aliases() -> None:
    names = {
        "TAIFEX": TAIFEXExchangeCalendar,
        "XTAF": TAIFEXExchangeCalendar,
        "TAIFEX_TX": TAIFEXExchangeCalendar,
        "TAIFEX_Day": TAIFEXDayCalendar,
    }

    calendars = {name: mcal.get_calendar(name) for name in names}

    for name, cls in names.items():
        assert type(calendars[name]) is cls
    assert calendars["XTAF"].name == "TAIFEX"
    assert calendars["TAIFEX_Day"].name == "TAIFEX_Day"
    assert calendars["TAIFEX"].full_name == "Taiwan Futures Exchange"
    assert calendars["TAIFEX"].tz == TPE
    assert TAIFEXExchangeCalendar().market_times == list(ALL_TIMES)
    # names round-trip through the registry and have their own sources, not the exchange_calendars fallback
    for name in ("TAIFEX", "TAIFEX_Day"):
        assert mcal.get_calendar(name).name == name
        assert any("taifex.com.tw" in source.url for source in mcal.get_calendar(name).sources)


def test_trading_days_match_taifex_data() -> None:
    expected = pd.bdate_range(FIRST_DAY, LAST_DAY).difference(session_exceptions("closed"))

    actual = TAIFEXExchangeCalendar().valid_days(FIRST_DAY, LAST_DAY, tz=None)

    assert actual.difference(expected).strftime("%Y-%m-%d").tolist() == []
    assert expected.difference(actual).strftime("%Y-%m-%d").tolist() == []
    assert len(actual) == 6107
    assert TAIFEXDayCalendar().valid_days(FIRST_DAY, LAST_DAY, tz=None).equals(actual)


def test_saturday_sessions_are_not_trading_days() -> None:
    # TAIFEX traded on make-up Saturdays until 2018; a Monday-Friday weekmask cannot express them (issue #480)
    saturdays = session_exceptions("saturday_session")

    actual = TAIFEXExchangeCalendar().valid_days(FIRST_DAY, LAST_DAY, tz=None)

    assert len(saturdays) == 23
    assert (saturdays.day_of_week == 5).all()
    assert saturdays.max() == pd.Timestamp("2018-12-22")
    assert not saturdays.isin(actual).any()


def test_after_hours_sessions_match_taifex_data() -> None:
    cal = TAIFEXExchangeCalendar()
    no_after_hours = session_exceptions("no_after_hours")

    schedule = cal.schedule("2017-05-15", LAST_DAY, tz=TPE)

    local = schedule.apply(lambda column: column.dt.tz_localize(None))
    previous_day = local.index.to_series().shift(1)
    with_session = local.index >= pd.Timestamp("2017-05-16")
    with_session &= ~local.index.isin(no_after_hours)
    # trading days with an after-hours session open at 15:00 on the previous trading day and pause at 05:00 after it
    opens = local.loc[with_session, "market_open"]
    night_closes = local.loc[with_session, "night_close"]
    assert (opens == previous_day[with_session] + pd.Timedelta(hours=15)).all()
    assert (night_closes == previous_day[with_session] + pd.Timedelta(hours=29)).all()
    # the others open at the regular 08:45 open
    day_only = local.loc[~with_session]
    assert day_only.index.strftime("%Y-%m-%d").tolist() == ["2017-05-15", *no_after_hours.strftime("%Y-%m-%d")]
    assert (day_only["market_open"] == day_only.index + pd.Timedelta(hours=8, minutes=45)).all()
    assert (day_only["night_close"] == day_only["market_open"]).all()
    # 2,321 after-hours sessions in the data, less the four that counted toward Saturday sessions in 2017-2018
    assert with_session.sum() == 2317


@pytest.mark.parametrize(
    "day, expected",
    [
        # first after-hours session, opened on 2017-05-15
        ("2017-05-16", ["Mon 05-15 15:00", "Tue 05-16 05:00", "Tue 05-16 08:45", "Tue 05-16 13:45"]),
        # regular weekday
        ("2026-10-28", ["Tue 10-27 15:00", "Wed 10-28 05:00", "Wed 10-28 08:45", "Wed 10-28 13:45"]),
        # Monday: Friday's session runs into Saturday morning
        ("2026-11-23", ["Fri 11-20 15:00", "Sat 11-21 05:00", "Mon 11-23 08:45", "Mon 11-23 13:45"]),
        # first day after Lunar New Year: the last evening before the break counts toward it
        ("2026-02-23", ["Wed 02-11 15:00", "Thu 02-12 05:00", "Mon 02-23 08:45", "Mon 02-23 13:45"]),
        # Dragon Boat Festival on Friday 2026-06-19
        ("2026-06-22", ["Thu 06-18 15:00", "Fri 06-19 05:00", "Mon 06-22 08:45", "Mon 06-22 13:45"]),
        # Typhoon Bavi closure on Friday 2026-07-10
        ("2026-07-13", ["Thu 07-09 15:00", "Fri 07-10 05:00", "Mon 07-13 08:45", "Mon 07-13 13:45"]),
        # Typhoon Champi closure on Friday 2026-10-23, then Retrocession Day observed on Monday 2026-10-26
        ("2026-10-27", ["Thu 10-22 15:00", "Fri 10-23 05:00", "Tue 10-27 08:45", "Tue 10-27 13:45"]),
        # announced 2027 Lunar New Year break: last trading day 2027-02-01
        ("2027-02-11", ["Mon 02-01 15:00", "Tue 02-02 05:00", "Thu 02-11 08:45", "Thu 02-11 13:45"]),
    ],
)
def test_after_hours_session_opens_on_previous_trading_day(day: str, expected: list[str]) -> None:
    cal = TAIFEXExchangeCalendar()

    schedule = cal.schedule(day, day)

    assert times(schedule, day) == expected


@pytest.mark.parametrize(
    "day",
    [
        "2017-05-15",  # before the after-hours launch
        "2017-06-05",  # Monday after the Saturday make-up session on 2017-06-03
        "2018-07-11",  # the 2018-07-10 evening session was closed for Typhoon Maria
        "2018-12-24",  # Monday after the last Saturday make-up session, 2018-12-22
    ],
)
def test_days_without_after_hours_session_open_at_0845(day: str) -> None:
    cal = TAIFEXExchangeCalendar()
    label = pd.Timestamp(day).strftime("%a %m-%d")

    schedule = cal.schedule(day, day)
    unforced = cal.schedule(day, day, force_special_times=False)

    assert times(schedule, day) == [f"{label} 08:45"] * 3 + [f"{label} 13:45"]
    assert times(unforced, day) == [f"{label} 08:45"] * 3 + [f"{label} 13:45"]


def test_regular_session_before_2001() -> None:
    cal, day_cal = TAIFEXExchangeCalendar(), TAIFEXDayCalendar()

    schedule = cal.schedule("2000-12-29", "2001-01-02")
    day_schedule = day_cal.schedule("2000-12-29", "2001-01-02")

    # 09:00-12:15 until the 2001-01-02 extension to 08:45-13:45
    assert times(schedule, "2000-12-29") == ["Fri 12-29 09:00"] * 3 + ["Fri 12-29 12:15"]
    assert times(schedule, "2001-01-02") == ["Tue 01-02 08:45"] * 3 + ["Tue 01-02 13:45"]
    assert times(day_schedule, "2000-12-29", ("market_open", "market_close")) == ["Fri 12-29 09:00", "Fri 12-29 12:15"]
    assert times(day_schedule, "2001-01-02", ("market_open", "market_close")) == ["Tue 01-02 08:45", "Tue 01-02 13:45"]


def test_day_calendar_has_regular_session_only() -> None:
    cal = TAIFEXDayCalendar()

    schedule = cal.schedule("2026-10-22", "2026-10-28")

    assert cal.market_times == ["market_open", "market_close"]
    assert schedule.index.strftime("%Y-%m-%d").tolist() == ["2026-10-22", "2026-10-27", "2026-10-28"]
    assert times(schedule, "2026-10-28", ("market_open", "market_close")) == ["Wed 10-28 08:45", "Wed 10-28 13:45"]
    assert cal.open_at_time(schedule, tpe("2026-10-27 09:00")) is True
    assert cal.open_at_time(schedule, tpe("2026-10-27 22:00")) is False


def test_closures_2026_and_2027() -> None:
    cal = TAIFEXExchangeCalendar()

    closed = {
        year: pd.bdate_range(f"{year}-01-01", f"{year}-12-31")
        .difference(cal.valid_days(f"{year}-01-01", f"{year}-12-31", tz=None))
        .strftime("%m-%d")
        .tolist()
        for year in (2026, 2027)
    }

    # TAIFEX 2026 calendar, incl. the no-trading days 02-12/02-13 and the typhoon days 07-10 and 10-23
    assert closed[2026] == [
        "01-01",
        "02-12",
        "02-13",
        "02-16",
        "02-17",
        "02-18",
        "02-19",
        "02-20",
        "02-27",
        "04-03",
        "04-06",
        "05-01",
        "06-19",
        "07-10",
        "09-25",
        "09-28",
        "10-09",
        "10-23",
        "10-26",
        "12-25",
    ]
    # TAIFEX 2027 calendar, announced 2026-11-10
    assert closed[2027] == [
        "01-01",
        "02-02",
        "02-03",
        "02-04",
        "02-05",
        "02-08",
        "02-09",
        "02-10",
        "03-01",
        "04-05",
        "04-06",
        "04-30",
        "06-09",
        "09-15",
        "09-28",
        "10-11",
        "10-25",
        "12-24",
        "12-31",
    ]


def test_open_at_time_across_after_hours_and_closures() -> None:
    cal = TAIFEXExchangeCalendar()

    lunar_new_year = cal.schedule("2026-02-10", "2026-02-24")
    weekend = cal.schedule("2026-11-19", "2026-11-24")

    # the last evening before Lunar New Year trades, and counts toward 2026-02-23
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-11 14:00")) is False
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-11 22:00")) is True
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-12 04:59")) is True
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-12 06:00")) is False
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-12 10:00")) is False
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-23 08:30")) is False
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-23 09:00")) is True
    assert cal.open_at_time(lunar_new_year, tpe("2026-02-23 15:00")) is True
    # Friday's after-hours session runs into Saturday morning, then nothing until Monday 08:45
    assert cal.open_at_time(weekend, tpe("2026-11-21 02:00")) is True
    assert cal.open_at_time(weekend, tpe("2026-11-21 06:00")) is False
    assert cal.open_at_time(weekend, tpe("2026-11-23 06:00")) is False
    assert cal.open_at_time(weekend, tpe("2026-11-23 08:45")) is True
