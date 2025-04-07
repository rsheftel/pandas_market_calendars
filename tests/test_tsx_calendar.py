import pandas as pd
from zoneinfo import ZoneInfo
from pandas.testing import assert_index_equal

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
