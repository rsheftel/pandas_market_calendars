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
