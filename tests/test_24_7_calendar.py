import pandas as pd
from pandas.testing import assert_index_equal

import pandas_market_calendars as mcal


def test_weekends():
    actual = mcal.get_calendar("24/7").schedule("2012-07-01", "2012-07-10").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2012-07-01"),
            pd.Timestamp("2012-07-02"),
            pd.Timestamp("2012-07-03"),
            pd.Timestamp("2012-07-04"),
            pd.Timestamp("2012-07-05"),
            pd.Timestamp("2012-07-06"),
            pd.Timestamp("2012-07-07"),
            pd.Timestamp("2012-07-08"),
            pd.Timestamp("2012-07-09"),
            pd.Timestamp("2012-07-10"),
        ]
    )

    assert_index_equal(actual, expected)
