import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.cme import CMEBondExchangeCalendar


def test_time_zone():
    assert CMEBondExchangeCalendar().tz == ZoneInfo("America/Chicago")
    assert CMEBondExchangeCalendar().name == "CME_Bond"


def test_sunday_opens():
    cme = CMEBondExchangeCalendar()
    schedule = cme.schedule("2020-01-01", "2020-01-31", tz="America/Chicago")
    assert (
        pd.Timestamp("2020-01-12 17:00:00", tz="America/Chicago")
        == schedule.loc["2020-01-13", "market_open"]
    )


def test_2020_full_holidays():
    # good friday: 2020-04-10
    # new years (observed): 2016-01-01
    # christmas (observed): 2020-12-25
    cme = CMEBondExchangeCalendar()
    good_dates = cme.valid_days("2020-01-01", "2020-12-31")
    for date in ["2020-04-10", "2020-01-01", "2020-12-25"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_2020_noon_holidays():
    # MLK: 2020-01-20
    # Presidents Day: 2020-02-17
    # Memorial Day: 2020-05-25
    # Labor Day: 2020-09-07
    # Thanksgiving: 2020-11-26
    cme = CMEBondExchangeCalendar()
    schedule = cme.schedule("2020-01-01", "2020-12-31")
    for date in ["2020-01-20", "2020-02-17", "2020-05-25", "2020-09-07", "2020-11-26"]:
        assert schedule.loc[date, "market_close"] == pd.Timestamp(date, tz="America/Chicago").replace(
            hour=12
        ).tz_convert("UTC")


def test_2020_noon_15_holidays():
    # Black Friday: 2020-11-27
    # Christmas Eve: 2020-12-24
    cme = CMEBondExchangeCalendar()
    schedule = cme.schedule("2020-11-27", "2020-12-24")
    for date in ["2020-11-27", "2020-12-24"]:
        assert schedule.loc[date, "market_close"] == pd.Timestamp(date, tz="America/Chicago").replace(
            hour=12, minute=15
        ).tz_convert("UTC")


def test_good_fridays():
    cme = CMEBondExchangeCalendar()
    schedule = cme.schedule("2020-01-01", "2021-12-31")
    assert pd.Timestamp("2020-04-10") not in schedule.index

    # Good Friday when it is the first friday of the month, open with early close
    assert pd.Timestamp("2021-04-02") in schedule.index
    assert schedule.loc[pd.Timestamp("2021-04-02"), "market_close"] == pd.Timestamp(
        "2021-04-02", tz="America/Chicago"
    ).replace(hour=10, minute=00).tz_convert("UTC")
