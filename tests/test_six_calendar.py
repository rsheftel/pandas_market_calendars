import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.six import SIXExchangeCalendar


def test_time_zone():
    assert SIXExchangeCalendar().tz == ZoneInfo("Europe/Zurich")
    assert SIXExchangeCalendar().name == "SIX"


def test_2018_holidays():
    # good friday: 2018-04-14
    # May 1st: 2018-05-01
    # christmas (observed): 2018-12-25
    # new years (observed): on a weekend, not rolled forward
    # https://www.six-group.com/exchanges/download/participants/regulation/trading_guides/trading_calendar_2018.pdf
    six = SIXExchangeCalendar()
    good_dates = six.valid_days("2018-01-01", "2018-12-31", tz="Europe/Zurich")

    for date in ["2018-05-24", "2018-06-15", "2018-03-23", "2018-12-21", "2018-12-27"]:
        assert pd.Timestamp(date, tz="Europe/Berlin") in good_dates
    for date in [
        "2018-01-01",
        "2018-01-02",
        "2018-03-30",
        "2018-04-02",
        "2018-05-01",
        "2018-05-10",
        "2018-05-21",
        "2018-08-01",
        "2018-12-24",
        "2018-12-25",
        "2018-12-26",
        "2018-12-31",
    ]:
        assert pd.Timestamp(date, tz="Europe/Zurich") not in good_dates


def test_eve_day_weekend():
    # christmas eve (observed): on a weekend
    # christmas (observed): 2017-12-25
    # boxing day (observed): 2017-12-26
    # https://www.six-group.com/exchanges/download/participants/regulation/trading_guides/trading_calendar_2017.pdf
    six = SIXExchangeCalendar()
    good_dates = six.valid_days("2017-12-01", "2017-12-31", tz="Europe/Zurich")

    for date in ["2017-12-22", "2017-12-27"]:
        assert pd.Timestamp(date, tz="Europe/Berlin") in good_dates
    for date in ["2017-12-24", "2017-12-25", "2017-12-26"]:
        assert pd.Timestamp(date, tz="Europe/Zurich") not in good_dates


def test_christmas_weekend():
    # christmas eve (observed): on a weekend
    # christmas (observed): on a weekend
    # boxing day (observed): 2016-12-26
    # https://www.six-group.com/exchanges/download/participants/regulation/trading_guides/trading_calendar_2016.pdf
    six = SIXExchangeCalendar()
    good_dates = six.valid_days("2016-12-01", "2016-12-31", tz="Europe/Zurich")

    for date in ["2016-12-22", "2016-12-23", "2016-12-27"]:
        assert pd.Timestamp(date, tz="Europe/Berlin") in good_dates
    for date in ["2016-12-24", "2016-12-25", "2016-12-26"]:
        assert pd.Timestamp(date, tz="Europe/Zurich") not in good_dates


def test_boxing_day_weekend():
    # christmas eve (observed): 2020-12-24
    # christmas (observed): 2020-12-25
    # boxing day (observed): on a weekend, not rolled forward
    # https://www.six-group.com/exchanges/download/participants/regulation/trading_guides/trading_calendar_2020.pdf
    six = SIXExchangeCalendar()
    good_dates = six.valid_days("2020-12-01", "2020-12-31", tz="Europe/Zurich")

    for date in ["2020-12-22", "2020-12-22", "2020-12-28"]:
        assert pd.Timestamp(date, tz="Europe/Berlin") in good_dates
    for date in ["2020-12-24", "2020-12-25", "2020-12-26", "2020-12-27"]:
        assert pd.Timestamp(date, tz="Europe/Zurich") not in good_dates
