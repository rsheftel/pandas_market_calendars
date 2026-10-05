import datetime

import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.hkex import HKEXExchangeCalendar


def test_time_zone():
    assert HKEXExchangeCalendar().tz == ZoneInfo("Asia/Shanghai")
    assert HKEXExchangeCalendar().name == "HKEX"


def test_2018_holidays():
    hkex = HKEXExchangeCalendar()
    trading_days = hkex.valid_days("2018-01-01", "2018-12-31")
    holidays = [
        "2018-01-01",
        "2018-02-16",
        "2018-02-17",
        "2018-02-18",
        "2018-02-19",
        "2018-03-30",
        "2018-04-02",
        "2018-04-05",
        "2018-05-01",
        "2018-05-22",
        "2018-06-18",
        "2018-07-02",
        "2018-09-25",
        "2018-10-01",
        "2018-10-17",
        "2018-12-25",
        "2018-12-26",
    ]
    for date in holidays:
        assert pd.Timestamp(date, tz="UTC") not in trading_days
    for date in ["2018-05-02"]:
        assert pd.Timestamp(date, tz="UTC") in trading_days


def test_2026_easter_ching_ming_overlap():
    # Ching Ming 2026 falls on Sunday Apr 5; its substitute (Mon Apr 6)
    # coincides with Easter Monday, so Tue Apr 7 is an additional general
    # holiday and HKEX is closed.
    hkex = HKEXExchangeCalendar()
    trading_days = hkex.valid_days("2026-04-01", "2026-04-10")
    for date in ["2026-04-03", "2026-04-06", "2026-04-07"]:
        assert pd.Timestamp(date, tz="UTC") not in trading_days
    for date in ["2026-04-01", "2026-04-02", "2026-04-08"]:
        assert pd.Timestamp(date, tz="UTC") in trading_days


def test_hkex_closes_at_lunch():
    hkex = HKEXExchangeCalendar()
    schedule = hkex.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=ZoneInfo("Asia/Shanghai")),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert hkex.open_at_time(
        schedule=schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert not hkex.open_at_time(
        schedule=schedule,
        timestamp=datetime.datetime(2015, 1, 14, 12, 10, tzinfo=ZoneInfo("Asia/Shanghai")),
    )
