import datetime

import pandas as pd
import pytest
from zoneinfo import ZoneInfo

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.china_futures import (
    CFFEXBondExchangeCalendar,
    CFFEXExchangeCalendar,
    CZCENightCalendar,
    DCENightCalendar,
    GFEXExchangeCalendar,
    INECrudeCalendar,
    SHFEBaseMetalsCalendar,
    SHFEExchangeCalendar,
    SHFEIndustrialsCalendar,
    SHFEPreciousMetalsCalendar,
)
from pandas_market_calendars.holidays.cn import all_holidays


SH = ZoneInfo("Asia/Shanghai")


def sh(ts):
    return pd.Timestamp(ts, tz=SH)


def times(schedule, columns):
    """Return the requested columns of a one-row schedule as 'Www mm-dd HH:MM' strings in Beijing time."""
    row = schedule.iloc[0]
    return [row[c].tz_convert(SH).strftime("%a %m-%d %H:%M") for c in columns]


def test_registry_and_aliases():
    for name, cls in [
        ("SHFE", SHFEExchangeCalendar),
        ("SHFE_CU", SHFEBaseMetalsCalendar),
        ("SHFE_AU", SHFEPreciousMetalsCalendar),
        ("SHFE_RB", SHFEIndustrialsCalendar),
        ("INE_SC", INECrudeCalendar),
        ("DCE_I", DCENightCalendar),
        ("CZCE_TA", CZCENightCalendar),
        ("ZCE", mcal.calendars.china_futures.CZCEExchangeCalendar),
        ("GFEX", GFEXExchangeCalendar),
        ("CFFEX_IF", CFFEXExchangeCalendar),
        ("CFFEX_T", CFFEXBondExchangeCalendar),
    ]:
        assert isinstance(mcal.get_calendar(name), cls)
    assert SHFEBaseMetalsCalendar().tz == ZoneInfo("Asia/Shanghai")
    assert SHFEBaseMetalsCalendar().name == "SHFE_BaseMetals"


def test_closures_follow_sse():
    cal = SHFEExchangeCalendar()
    holidays = pd.DatetimeIndex(all_holidays)
    trading_days = cal.valid_days(holidays.min(), holidays.max())
    assert not holidays.tz_localize("UTC").isin(trading_days).any()

    # National Day 2026 (1-7 Oct), the Sunday 27 Sep and Saturday 10 Oct make-up workdays are not trading days.
    days = cal.valid_days("2026-09-24", "2026-10-13", tz=None).strftime("%Y-%m-%d").tolist()
    assert days == [
        "2026-09-24",
        "2026-09-28",
        "2026-09-29",
        "2026-09-30",
        "2026-10-08",
        "2026-10-09",
        "2026-10-12",
        "2026-10-13",
    ]


def test_day_session():
    sched = SHFEExchangeCalendar().schedule("2026-10-27", "2026-10-27")
    assert list(sched.columns) == [
        "market_open",
        "pause_start",
        "pause_end",
        "break_start",
        "break_end",
        "market_close",
    ]
    assert times(sched, sched.columns) == [
        "Tue 10-27 09:00",
        "Tue 10-27 10:15",
        "Tue 10-27 10:30",
        "Tue 10-27 11:30",
        "Tue 10-27 13:30",
        "Tue 10-27 15:00",
    ]
    sched = SHFEExchangeCalendar().schedule("2026-10-05", "2026-10-30")
    assert SHFEExchangeCalendar().open_at_time(sched, sh("2026-10-27 10:20")) is False  # morning pause
    assert SHFEExchangeCalendar().open_at_time(sched, sh("2026-10-27 12:00")) is False  # lunch
    assert SHFEExchangeCalendar().open_at_time(sched, sh("2026-10-27 14:00")) is True
    assert (
        SHFEExchangeCalendar().open_at_time(sched, sh("2026-10-27 22:00")) is False
    )  # no night session on this calendar


def test_cffex_sessions():
    equity = CFFEXExchangeCalendar().schedule("2026-10-27", "2026-10-27")
    assert times(equity, ["market_open", "break_start", "break_end", "market_close"]) == [
        "Tue 10-27 09:30",
        "Tue 10-27 11:30",
        "Tue 10-27 13:00",
        "Tue 10-27 15:00",
    ]
    bond = CFFEXBondExchangeCalendar().schedule("2026-10-27", "2026-10-27")
    assert times(bond, ["market_close"]) == ["Tue 10-27 15:15"]
    assert "night_close" not in GFEXExchangeCalendar().market_times


@pytest.mark.parametrize(
    "cls, night_close",
    [
        (SHFEBaseMetalsCalendar, "Tue 10-27 01:00"),
        (SHFEPreciousMetalsCalendar, "Tue 10-27 02:30"),
        (SHFEIndustrialsCalendar, "Mon 10-26 23:00"),
        (INECrudeCalendar, "Tue 10-27 02:30"),
        (DCENightCalendar, "Mon 10-26 23:00"),
        (CZCENightCalendar, "Mon 10-26 23:00"),
    ],
)
def test_night_session_belongs_to_next_trading_day(cls, night_close):
    sched = cls().schedule("2026-10-27", "2026-10-27")
    assert times(sched, ["market_open", "night_close", "day_open", "market_close"]) == [
        "Mon 10-26 21:00",
        night_close,
        "Tue 10-27 09:00",
        "Tue 10-27 15:00",
    ]


@pytest.mark.parametrize(
    "cls, night_close",
    [
        (SHFEBaseMetalsCalendar, "Sat 10-24 01:00"),
        (SHFEPreciousMetalsCalendar, "Sat 10-24 02:30"),
        (SHFEIndustrialsCalendar, "Fri 10-23 23:00"),
    ],
)
def test_monday_trading_day_starts_friday_evening(cls, night_close):
    sched = cls().schedule("2026-10-26", "2026-10-26")
    assert times(sched, ["market_open", "night_close", "day_open"]) == [
        "Fri 10-23 21:00",
        night_close,
        "Mon 10-26 09:00",
    ]


@pytest.mark.parametrize(
    "first_day_after_closure",
    [
        "2026-01-05",  # Monday after the New Year closure (1-2 Jan)
        "2026-02-24",  # Spring Festival
        "2026-04-07",  # Tuesday after Qingming Monday
        "2026-05-06",  # Labour Day
        "2026-06-22",  # Monday after Dragon Boat Friday
        "2026-09-28",  # Monday after Mid-Autumn Friday
        "2026-10-08",  # National Day
    ],
)
def test_no_night_session_after_holiday(first_day_after_closure):
    cal = SHFEBaseMetalsCalendar()
    sched = cal.schedule(first_day_after_closure, first_day_after_closure)
    opens = times(sched, ["market_open", "night_close", "day_open"])
    assert opens[0] == opens[1] == opens[2]
    assert opens[0].endswith(f"{first_day_after_closure[5:]} 09:00")


def test_open_at_time_across_night_and_holiday():
    cal = SHFEBaseMetalsCalendar()
    sched = cal.schedule("2026-09-28", "2026-10-20")
    assert cal.open_at_time(sched, sh("2026-10-07 22:00")) is False  # evening before the first day back
    assert cal.open_at_time(sched, sh("2026-10-08 00:30")) is False
    assert cal.open_at_time(sched, sh("2026-10-08 09:00")) is True
    assert cal.open_at_time(sched, sh("2026-10-08 22:00")) is True  # night session of trading day 2026-10-09
    assert cal.open_at_time(sched, sh("2026-10-09 00:30")) is True
    assert cal.open_at_time(sched, sh("2026-10-09 01:30")) is False
    assert cal.open_at_time(sched, sh("2026-10-10 00:30")) is True  # Friday night runs into Saturday
    assert cal.open_at_time(sched, sh("2026-10-11 22:00")) is False  # no Sunday session
    assert cal.open_at_time(sched, sh("2026-10-12 00:30")) is False
    assert cal.open_at_time(sched, sh("2026-10-13 10:20")) is False
    industrials = SHFEIndustrialsCalendar()
    sched = industrials.schedule("2026-09-28", "2026-10-20")
    assert industrials.open_at_time(sched, sh("2026-10-13 00:30")) is False  # night closed at 23:00


def test_night_session_suspended_in_2020():
    cal = SHFEBaseMetalsCalendar()
    sched = cal.schedule("2020-01-23", "2020-05-08")
    assert times(sched.loc[["2020-01-23"]], ["market_open"]) == ["Wed 01-22 21:00"]
    for day in ["2020-02-03", "2020-02-10", "2020-05-06"]:
        assert times(sched.loc[[day]], ["market_open"])[0].endswith(f"{day[5:]} 09:00")
    assert times(sched.loc[["2020-05-07"]], ["market_open"]) == ["Wed 05-06 21:00"]


def test_before_night_trading_started():
    sched = SHFEBaseMetalsCalendar().schedule("2013-12-19", "2013-12-20")
    assert times(sched.loc[["2013-12-19"]], ["market_open", "night_close"]) == [
        "Thu 12-19 09:00",
        "Thu 12-19 09:00",
    ]
    assert times(sched.loc[["2013-12-20"]], ["market_open", "night_close"]) == [
        "Thu 12-19 21:00",
        "Fri 12-20 01:00",
    ]


def test_schedule_tz_argument():
    sched = SHFEBaseMetalsCalendar().schedule("2026-10-27", "2026-10-27", tz="Asia/Shanghai")
    assert sched.iloc[0]["market_open"] == datetime.datetime(2026, 10, 26, 21, tzinfo=SH)
