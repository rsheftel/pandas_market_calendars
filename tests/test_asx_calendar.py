from itertools import chain
from zoneinfo import ZoneInfo

import pandas as pd

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
    australia_unique_hols = {i: {"closed": None, "open": None} for i in australia_unique_hols_names}

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


def test_2011_easter_tuesday_holiday():
    # 2011/04/26 - Easter Tuesday / Public Holiday (ANZAC Day fell on Easter Monday)
    # https://web.archive.org/web/20110525134520/http://www.asx.com.au/about/asx-trading-calendar-2011.htm
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days("2011-04-01", "2011-04-30")
    assert pd.Timestamp("2011-04-26", tz="UTC") not in good_dates
    assert pd.Timestamp("2011-04-27", tz="UTC") in good_dates


def test_christmas_and_new_years_eve_early_closes():
    asx = ASXExchangeCalendar()

    # Before 2022, a weekend Christmas Eve or New Year's Eve moved the 14:10 early close to the previous Friday
    # https://web.archive.org/web/20110525134520/http://www.asx.com.au/about/asx-trading-calendar-2011.htm
    schedule = asx.schedule("2011-12-01", "2011-12-31")
    early_closes = asx.early_closes(schedule).index
    for date in ["2011-12-23", "2011-12-30"]:
        assert pd.Timestamp(date) in early_closes
        assert schedule.loc[date, "market_close"].tz_convert(asx.tz).strftime("%H:%M") == "14:10"

    # From 2022, ASX traded a full day on the Friday before a weekend Christmas Eve or New Year's Eve
    # https://web.archive.org/web/20220321145452/https://www.asx.com.au/markets/market-resources/trading-hours-calendar/cash-market-trading-hours/trading-calendar
    # https://web.archive.org/web/20230713033224/https://www2.asx.com.au/markets/market-resources/trading-hours-calendar/cash-market-trading-hours/trading-calendar
    schedule = asx.schedule("2022-12-01", "2023-12-31")
    early_closes = asx.early_closes(schedule).index
    for date in ["2022-12-23", "2022-12-30", "2023-12-22", "2023-12-29"]:
        assert pd.Timestamp(date) in schedule.index
        assert pd.Timestamp(date) not in early_closes

    # A weekday Christmas Eve or New Year's Eve is still an early close
    schedule = asx.schedule("2025-12-01", "2025-12-31")
    early_closes = asx.early_closes(schedule).index
    for date in ["2025-12-24", "2025-12-31"]:
        assert pd.Timestamp(date) in early_closes
