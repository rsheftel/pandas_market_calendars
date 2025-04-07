from itertools import chain

import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.asx import ASXExchangeCalendar


def test_time_zone():
    assert ASXExchangeCalendar().tz == ZoneInfo("Australia/Sydney")


def test_2019_holidays():
    # 2019/01/28 - Australia Day (additional day)
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days("2019-01-01", "2019-12-31")
    for date in ["2019-01-28"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_2021_holidays():
    # 2021/01/26 - Australia Day
    # 2021/12/27 - Christmas (additional day)
    # 2021/12/28 - Boxing Day (additional day)
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days("2021-01-01", "2021-12-31")
    for date in ["2021-01-26", "2021-12-27", "2021-12-28"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_2022_holidays():
    # 2022/01/26 - Australia Day
    # 2022/12/25 - Christmas
    # 2022/12/26 - Boxing Day
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days("2022-01-01", "2022-12-31")
    for date in ["2022-01-26", "2022-12-25", "2022-12-26"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_unique_holidays():
    australia_unique_hols_names = ["QEII_DayOfMourning"]
    australia_unique_hols = {
        i: {"closed": None, "open": None} for i in australia_unique_hols_names
    }

    # One-off holiday additions and removals in Australia

    # National Day of Mourning for Her Majesty the Queen
    australia_unique_hols["QEII_DayOfMourning"]["closed"] = [pd.Timestamp("2022-09-22")]

    # Test of closed dates
    asx = ASXExchangeCalendar()
    # get all the closed dates
    closed_days = [australia_unique_hols[k].get("closed") for k in australia_unique_hols]
    good_dates = asx.valid_days("1990-01-01", "2022-12-31")
    for date in chain.from_iterable(closed_days):
        assert pd.Timestamp(date, tz="UTC") not in good_dates

    # Test of open dates
    open_days = [australia_unique_hols[k].get("open") for k in australia_unique_hols]
    open_days = [i for i in open_days if i]
    good_dates = asx.valid_days("1990-01-01", "2022-12-31")
    for date in chain.from_iterable(open_days):
        assert pd.Timestamp(date, tz="UTC") in good_dates
