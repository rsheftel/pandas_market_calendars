from zoneinfo import ZoneInfo

import pandas as pd

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.forex import ForexExchangeCalendar


def test_name():
    assert ForexExchangeCalendar().name == "FOREX"


def test_aliases():
    assert "FOREX" in mcal.get_calendar_names()
    assert "FX" in mcal.get_calendar_names()
    assert "Forex" in mcal.get_calendar_names()


def test_timezone():
    cal = ForexExchangeCalendar()
    assert cal.tz == ZoneInfo("America/New_York")


def test_weekmask():
    cal = ForexExchangeCalendar()
    assert cal.weekmask == "Mon Tue Wed Thu Fri"


def test_no_holidays():
    cal = ForexExchangeCalendar()
    valid_days = cal.valid_days("2024-01-01", "2024-01-31")
    assert pd.Timestamp("2024-01-01", tz="UTC") in valid_days
    assert pd.Timestamp("2024-01-06", tz="UTC") not in valid_days
    assert pd.Timestamp("2024-01-07", tz="UTC") not in valid_days
    assert pd.Timestamp("2024-01-08", tz="UTC") in valid_days
    assert pd.Timestamp("2024-01-13", tz="UTC") not in valid_days
    assert pd.Timestamp("2024-01-14", tz="UTC") not in valid_days


def test_schedule_weekends():
    cal = ForexExchangeCalendar()
    schedule = cal.schedule("2024-01-01", "2024-01-14")
    assert pd.Timestamp("2024-01-06") not in schedule.index
    assert pd.Timestamp("2024-01-07") not in schedule.index
    assert pd.Timestamp("2024-01-13") not in schedule.index
    assert pd.Timestamp("2024-01-14") not in schedule.index
    assert pd.Timestamp("2024-01-01") in schedule.index
    assert pd.Timestamp("2024-01-08") in schedule.index


def test_schedule_times():
    cal = ForexExchangeCalendar()
    schedule = cal.schedule("2024-01-07", "2024-01-12", tz="America/New_York")
    monday_schedule = schedule.loc["2024-01-08"]
    monday_open_utc = monday_schedule["market_open"].tz_convert("UTC")
    assert monday_open_utc.hour == 22
    friday_schedule = schedule.loc["2024-01-12"]
    friday_close_utc = friday_schedule["market_close"].tz_convert("UTC")
    assert friday_close_utc.hour == 22


def test_open_on_holidays():
    cal = ForexExchangeCalendar()
    schedule = cal.schedule("2024-01-01", "2024-01-01")
    assert pd.Timestamp("2024-01-01") in schedule.index

    schedule = cal.schedule("2023-12-25", "2023-12-25")
    if pd.Timestamp("2023-12-25").weekday() != 5:
        assert pd.Timestamp("2023-12-25") in schedule.index


def test_sunday_evening_opens_monday_and_saturday_is_closed():
    cal = ForexExchangeCalendar()
    schedule = cal.schedule("2024-01-07", "2024-01-14", tz="America/New_York")
    assert pd.Timestamp("2024-01-07") not in schedule.index
    assert pd.Timestamp("2024-01-14") not in schedule.index
    monday = schedule.loc["2024-01-08"]
    assert monday["market_open"] == pd.Timestamp("2024-01-07 17:00", tz="America/New_York")
    assert monday["market_close"] == pd.Timestamp("2024-01-08 17:00", tz="America/New_York")
    assert not any(schedule["market_open"].dt.day_name() == "Saturday")
    assert not any(schedule["market_close"].dt.day_name() == "Saturday")
