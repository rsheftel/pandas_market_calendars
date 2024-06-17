import pandas as pd
from pandas.testing import assert_index_equal, assert_series_equal

import pandas_market_calendars as mcal


def test_xtae_schedule():
    actual = mcal.get_calendar("XTAE").schedule("2012-07-01", "2012-07-10").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2012-07-01"),
            pd.Timestamp("2012-07-02"),
            pd.Timestamp("2012-07-03"),
            pd.Timestamp("2012-07-04"),
            pd.Timestamp("2012-07-05"),
            pd.Timestamp("2012-07-08"),
            pd.Timestamp("2012-07-09"),
            pd.Timestamp("2012-07-10"),
        ]
    )

    assert_index_equal(actual, expected)


def test_xtae_sunday_close():
    actual = mcal.get_calendar("XTAE").schedule("2012-07-01", "2012-07-10")

    expected = pd.Series(
        index=[
            pd.Timestamp("2012-07-01"),
            pd.Timestamp("2012-07-02"),
            pd.Timestamp("2012-07-03"),
            pd.Timestamp("2012-07-04"),
            pd.Timestamp("2012-07-05"),
            pd.Timestamp("2012-07-08"),
            pd.Timestamp("2012-07-09"),
            pd.Timestamp("2012-07-10"),
        ],
        data=[
            pd.Timestamp("2012-07-01 12:40:00+00:00"),
            pd.Timestamp("2012-07-02 14:15:00+00:00"),
            pd.Timestamp("2012-07-03 14:15:00+00:00"),
            pd.Timestamp("2012-07-04 14:15:00+00:00"),
            pd.Timestamp("2012-07-05 14:15:00+00:00"),
            pd.Timestamp("2012-07-08 12:40:00+00:00"),
            pd.Timestamp("2012-07-09 14:15:00+00:00"),
            pd.Timestamp("2012-07-10 14:15:00+00:00"),
        ],
        name="market_close",
    )

    assert_series_equal(actual["market_close"], expected)
