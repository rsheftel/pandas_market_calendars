from datetime import time

import numpy as np
import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.iex import IEXExchangeCalendar
from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar
from pandas_market_calendars.class_registry import ProtectedDict


iex = IEXExchangeCalendar()


def test_time_zone():
    assert iex.tz == ZoneInfo("America/New_York")
    assert iex.name == "IEX"


def test_open_close():
    assert iex.open_time == time(9, 30, tzinfo=ZoneInfo("America/New_York"))
    assert iex.close_time == time(16, tzinfo=ZoneInfo("America/New_York"))


def test_calendar_utility():
    assert len(iex.holidays().holidays) > 0
    assert isinstance(iex.regular_market_times, ProtectedDict)

    valid_days = iex.valid_days(start_date="2016-12-20", end_date="2017-01-10")
    assert isinstance(valid_days, pd.DatetimeIndex)
    assert not valid_days.empty

    schedule = iex.schedule(start_date="2015-07-01", end_date="2017-07-10", start="pre", end="post")
    assert isinstance(schedule, pd.DataFrame)
    assert not schedule.empty


def test_trading_days_before_operation():
    trading_days = iex.valid_days(start_date="2000-01-01", end_date="2022-02-23")
    assert np.array([~(trading_days <= "2013-08-25")]).any()

    trading_days = iex.date_range_htf("1D", "2000-01-01", "2022-02-23")
    assert np.array([~(trading_days <= "2013-08-25")]).any()

    trading_days = iex.date_range_htf("1D", "2000-01-01", "2010-02-23")
    assert len(trading_days) == 0


def test_holidays_and_early_closes():
    # https://www.iex.io/resources/trading/trading-hours-holidays
    valid_days = iex.valid_days(start_date="2025-01-01", end_date="2026-12-31")
    for holiday in ["2025-01-01", "2025-01-09", "2025-09-01", "2026-01-01", "2026-09-07"]:
        assert pd.Timestamp(holiday, tz="UTC") not in valid_days

    schedule = iex.schedule(start_date="2026-12-24", end_date="2026-12-24")
    assert schedule.loc["2026-12-24", "market_close"] == pd.Timestamp("2026-12-24 13:00", tz="America/New_York")


def test_schedule_matches_nyse():
    start, end = "2013-08-26", "2026-12-31"
    pd.testing.assert_frame_equal(iex.schedule(start, end), NYSEExchangeCalendar().schedule(start, end))
