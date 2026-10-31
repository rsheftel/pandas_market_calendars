"""
This tests the Tokyo Stock Exchange calendar from the exchange_calendars package that is brought in via the mirror
"""

import pandas as pd

import pandas_market_calendars as mcal


xtks_cal = mcal.get_calendar("XTKS")


def test_national_holidays_before_1997():
    # exchange_calendars starts XTKS in 1997; https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv
    holidays = [
        "1990-03-21",
        "1990-09-24",
        "1990-11-12",
        "1991-03-21",
        "1991-09-23",
        "1992-03-20",
        "1992-09-23",
        "1993-06-09",
        "1993-09-23",
        "1994-03-21",
        "1994-09-23",
        "1995-03-21",
        "1996-03-20",
        "1996-09-23",
    ]
    valid_days = xtks_cal.valid_days("1990-01-01", "1996-12-31")
    for day in holidays:
        assert pd.Timestamp(day, tz="UTC") not in valid_days


def test_days_next_to_the_holidays_stay_open():
    valid_days = xtks_cal.valid_days("1990-03-19", "1990-03-23")
    assert pd.Timestamp("1990-03-20", tz="UTC") in valid_days
    assert pd.Timestamp("1990-03-22", tz="UTC") in valid_days
