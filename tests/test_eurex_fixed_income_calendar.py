import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.eurex_fixed_income import (
    EUREXFixedIncomeCalendar,
)


def test_time_zone():
    assert EUREXFixedIncomeCalendar().tz == ZoneInfo("Europe/Berlin")
    assert EUREXFixedIncomeCalendar().name == "EUREX_Bond"


def _test_year_holiday(year, bad_dates):
    eurex = EUREXFixedIncomeCalendar()
    good_dates = eurex.valid_days(f"{year}-01-01", f"{year}-12-31")

    # Make sure holiday dates aren't in the schedule
    for date in bad_dates:
        assert pd.Timestamp(date, tz="UTC") not in good_dates

    # Make sure all other weekdays are in the schedule
    expected_good_dates = [
        d.strftime("%Y-%m-%d")
        for d in pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
        if d.weekday() < 5 and d.strftime("%Y-%m-%d") not in bad_dates
    ]
    for date in expected_good_dates:
        assert pd.Timestamp(date, tz="UTC") in good_dates


def test_2017_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 14 April, 17 April, 1 May, 25 December, 26 December
    """
    bad_dates = ["2017-04-14", "2017-04-17", "2017-05-01", "2017-12-25", "2017-12-26"]
    _test_year_holiday(2017, bad_dates)


def test_2018_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 1 January, 30 March, 2 April, 1 May, 25 December, 26 December
    Eurex is closed for trading in all derivatives: 24 December, 31 December
    """
    bad_dates = [
        "2018-01-01",
        "2018-03-30",
        "2018-04-02",
        "2018-05-01",
        "2018-12-24",
        "2018-12-25",
        "2018-12-26",
        "2018-12-31",
    ]
    _test_year_holiday(2018, bad_dates)


def test_2019_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 1 January, 19 April, 22 April, 1 May, 25 December, 26 December
    Eurex is closed for trading in all derivatives: 24 December, 31 December
    """
    bad_dates = [
        "2019-01-01",
        "2019-04-19",
        "2019-04-22",
        "2019-05-01",
        "2019-12-24",
        "2019-12-25",
        "2019-12-26",
        "2019-12-31",
    ]
    _test_year_holiday(2019, bad_dates)


def test_2020_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 1 January, 10 April, 13 April, 1 May, 25 December
    Eurex is closed for trading in all derivatives: 24 December, 31 December
    """
    bad_dates = [
        "2020-01-01",
        "2020-04-10",
        "2020-04-13",
        "2020-05-01",
        "2020-12-24",
        "2020-12-25",
        "2020-12-31",
    ]
    _test_year_holiday(2020, bad_dates)


def test_2021_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 1 January, 2 April, 5 April
    Eurex is closed for trading in all derivatives: 24 December, 31 December
    """
    bad_dates = [
        "2021-01-01",
        "2021-04-02",
        "2021-04-05",
        "2021-05-01",
        "2021-12-24",
        "2021-12-31",
    ]
    _test_year_holiday(2021, bad_dates)


def test_2022_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 15 April, 18 April, 26 December
    """
    bad_dates = ["2022-04-15", "2022-04-18", "2022-12-26"]
    _test_year_holiday(2022, bad_dates)


def test_2023_holidays():
    """
    Eurex is closed for trading and clearing (exercise, settlement and cash)
    in all derivatives: 7 April, 10 April, 1 May, 25 December, 26 December
    """
    bad_dates = ["2023-04-07", "2023-04-10", "2023-05-01", "2023-12-25", "2023-12-26"]
    _test_year_holiday(2023, bad_dates)


def test_2024_holidays():
    bad_dates = [
        "2024-01-01",
        "2024-03-29",
        "2024-04-01",
        "2024-05-01",
        "2024-12-24",
        "2024-12-25",
        "2024-12-26",
        "2024-12-31",
    ]
    _test_year_holiday(2024, bad_dates)
