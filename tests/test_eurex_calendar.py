import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.eurex import EUREXExchangeCalendar


def test_time_zone():
    assert EUREXExchangeCalendar().tz == ZoneInfo("Europe/Berlin")
    assert EUREXExchangeCalendar().name == "EUREX"


def test_2016_holidays():
    # good friday: 2016-03-25
    # May 1st: on a weekend, not rolled forward
    # christmas: on a weekend, not rolled forward
    # boxing day: 2016-12-26
    # new years (observed): 2016-01-01
    eurex = EUREXExchangeCalendar()
    good_dates = eurex.valid_days("2016-01-01", "2016-12-31")
    for date in ["2016-03-25", "2016-01-01", "2016-12-26"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates
    for date in ["2016-05-02"]:
        assert pd.Timestamp(date, tz="UTC") in good_dates


def test_2017_holidays():
    # good friday: 2017-04-14
    # May 1st: 2017-05-01
    # christmas (observed): 2017-12-25
    # new years (observed): on a weekend, not rolled forward
    eurex = EUREXExchangeCalendar()
    good_dates = eurex.valid_days("2017-01-01", "2017-12-31")
    for date in ["2016-04-14", "2017-05-01", "2017-12-25"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates
    for date in ["2017-01-02"]:
        assert pd.Timestamp(date, tz="UTC") in good_dates
