import datetime

import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.bmf import BMFExchangeCalendar


def test_time_zone():
    assert BMFExchangeCalendar().tz == ZoneInfo("America/Sao_Paulo")


def test_2020_holidays_skip():
    # 2020-07-09 - skipped due to covid
    # 2020-11-20 - skipped due to covid

    holidays = BMFExchangeCalendar().holidays().holidays
    for date in ["2019-07-09", "2019-11-20", "2021-07-09", "2021-11-20"]:
        assert pd.Timestamp(date, tz="UTC").to_datetime64() in holidays
    for date in ["2020-07-09", "2020-11-20"]:
        assert pd.Timestamp(date, tz="UTC").to_datetime64() not in holidays


def test_post_2022_regulation_change():
    # Regional holidays no longer observed: January 25th, July 9th, November 20th
    # November 20th was reinstated as a national holiday starting in 2024

    holidays = BMFExchangeCalendar().holidays().holidays

    for year in [2017, 2018, 2019, 2021]:  # skip 2020 due to test above
        for month, day in [(1, 25), (7, 9), (11, 20)]:
            assert (
                pd.Timestamp(datetime.date(year, month, day), tz="UTC").to_datetime64()
                in holidays
            )
    for year in range(2022, 2040):
        for month, day in [(1, 25), (7, 9)]:
            assert pd.Timestamp(datetime.date(year, month, day), tz="UTC").to_datetime64() not in holidays
    for year in range(2022, 2024):
        for month, day in [(11, 20)]:
            assert pd.Timestamp(datetime.date(year, month, day), tz="UTC").to_datetime64() not in holidays


def test_sunday_new_years_eve():
    # All instances of December 29th on a Friday should be holidays

    holidays = BMFExchangeCalendar().holidays().holidays

    for year in range(1994, 2040):
        date = pd.Timestamp(datetime.date(year, 12, 29), tz="UTC")
        if date.day_of_week == 4:
            # December 29th on a Friday

            assert date.to_datetime64() in holidays


def test_post_2022_nov20():
    # November 20th national holiday should be present from 2024

    holidays = BMFExchangeCalendar().holidays().holidays

    for year in range(2024, 2040):
        assert pd.Timestamp(datetime.date(year, 11, 20), tz="UTC").to_datetime64() in holidays
