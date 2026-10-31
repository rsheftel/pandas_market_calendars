import pandas as pd
from pandas.testing import assert_index_equal
from zoneinfo import ZoneInfo

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.tsx import TSXExchangeCalendar, VictoriaDay


def test_time_zone():
    assert TSXExchangeCalendar().tz == ZoneInfo("Canada/Eastern")
    assert TSXExchangeCalendar().name == "TSX"


def test_victoria_day():
    actual = VictoriaDay.dates("2009-01-01", "2020-12-31")

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2009-05-18"),
            pd.Timestamp("2010-05-24"),
            pd.Timestamp("2011-05-23"),
            pd.Timestamp("2012-05-21"),
            pd.Timestamp("2013-05-20"),
            pd.Timestamp("2014-05-19"),
            pd.Timestamp("2015-05-18"),
            pd.Timestamp("2016-05-23"),
            pd.Timestamp("2017-05-22"),
            pd.Timestamp("2018-05-21"),
            pd.Timestamp("2019-05-20"),
            pd.Timestamp("2020-05-18"),
        ]
    )

    assert_index_equal(actual, expected)


def test_christmas_eve_post_2010():
    cal = TSXExchangeCalendar()
    sched_2015 = cal.schedule("2015-12-20", "2015-12-26")
    assert sched_2015.loc[pd.Timestamp("2015-12-24"), "market_close"] == pd.Timestamp("2015-12-24 18:00 +0")


def test_christmas_eve_pre_2010():
    cal = TSXExchangeCalendar()
    sched_2009 = cal.schedule("2009-12-20", "2009-12-26")
    assert sched_2009.loc[pd.Timestamp("2009-12-24"), "market_close"] == pd.Timestamp("2009-12-24 21:00 +0")


def test_september_11_sessions() -> None:
    expected = pd.DatetimeIndex(["2001-09-10", "2001-09-11", "2001-09-13"], tz="UTC")

    assert_index_equal(TSXExchangeCalendar().valid_days("2001-09-10", "2001-09-13"), expected)
    assert_index_equal(mcal.get_calendar("TSXV").valid_days("2001-09-10", "2001-09-13"), expected)


def test_christmas_1993_sessions() -> None:
    expected = pd.DatetimeIndex(["1993-12-22", "1993-12-23", "1993-12-28", "1993-12-29"], tz="UTC")

    assert_index_equal(TSXExchangeCalendar().valid_days("1993-12-22", "1993-12-29"), expected)
    assert_index_equal(mcal.get_calendar("TSXV").valid_days("1993-12-22", "1993-12-29"), expected)


def test_boxing_day_before_1993() -> None:
    expected = pd.DatetimeIndex(["1992-12-22", "1992-12-23", "1992-12-24", "1992-12-29"], tz="UTC")

    assert_index_equal(TSXExchangeCalendar().valid_days("1992-12-22", "1992-12-29"), expected)


def test_christmas_1994_sessions() -> None:
    expected = pd.DatetimeIndex(["1994-12-22", "1994-12-23", "1994-12-28", "1994-12-29"], tz="UTC")

    assert_index_equal(TSXExchangeCalendar().valid_days("1994-12-22", "1994-12-29"), expected)


def test_christmas_saturday_2021_sessions() -> None:
    expected = pd.DatetimeIndex(["2021-12-22", "2021-12-23", "2021-12-24", "2021-12-29"], tz="UTC")

    assert_index_equal(TSXExchangeCalendar().valid_days("2021-12-22", "2021-12-29"), expected)
    assert_index_equal(mcal.get_calendar("TSXV").valid_days("2021-12-22", "2021-12-29"), expected)


def test_lse_boxing_day_observance_unchanged() -> None:
    cal = mcal.get_calendar("LSE")
    expected_1993 = pd.DatetimeIndex(["1993-12-22", "1993-12-23", "1993-12-24", "1993-12-29"], tz="UTC")
    expected_2021 = pd.DatetimeIndex(["2021-12-22", "2021-12-23", "2021-12-24", "2021-12-29"], tz="UTC")

    assert_index_equal(cal.valid_days("1993-12-22", "1993-12-29"), expected_1993)
    assert_index_equal(cal.valid_days("2021-12-22", "2021-12-29"), expected_2021)
