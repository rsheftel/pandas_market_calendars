import pandas as pd
from pandas.testing import assert_index_equal, assert_series_equal

import pandas_market_calendars as mcal


def test_tase_pre_2026_week_is_sunday_to_thursday():
    actual = mcal.get_calendar("TASE").schedule("2025-06-01", "2025-06-12").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2025-06-03"),  # Tue (Jun 1-2 closed for Shavuot)
            pd.Timestamp("2025-06-04"),
            pd.Timestamp("2025-06-05"),
            pd.Timestamp("2025-06-08"),  # Sun
            pd.Timestamp("2025-06-09"),
            pd.Timestamp("2025-06-10"),
            pd.Timestamp("2025-06-11"),
            pd.Timestamp("2025-06-12"),
        ]
    )

    assert_index_equal(actual, expected)


def test_tase_trading_week_transition():
    # Last Sunday session was 2026-01-04; Monday-Friday trading from 2026-01-05
    actual = mcal.get_calendar("TASE").schedule("2025-12-28", "2026-01-12").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2025-12-28"),  # Sun
            pd.Timestamp("2025-12-29"),
            pd.Timestamp("2025-12-30"),
            pd.Timestamp("2025-12-31"),
            pd.Timestamp("2026-01-01"),  # Thu
            pd.Timestamp("2026-01-04"),  # Sun, last Sunday session
            pd.Timestamp("2026-01-05"),  # Mon, first Monday-Friday week
            pd.Timestamp("2026-01-06"),
            pd.Timestamp("2026-01-07"),
            pd.Timestamp("2026-01-08"),
            pd.Timestamp("2026-01-09"),  # Fri, first Friday session
            pd.Timestamp("2026-01-12"),  # Mon (no Sunday session on Jan 11)
        ]
    )

    assert_index_equal(actual, expected)


def test_tase_friday_early_close():
    actual = mcal.get_calendar("TASE").schedule("2026-01-05", "2026-01-09")

    expected = pd.Series(
        index=[
            pd.Timestamp("2026-01-05"),
            pd.Timestamp("2026-01-06"),
            pd.Timestamp("2026-01-07"),
            pd.Timestamp("2026-01-08"),
            pd.Timestamp("2026-01-09"),
        ],
        data=[
            pd.Timestamp("2026-01-05 13:59:00+00:00"),
            pd.Timestamp("2026-01-06 13:59:00+00:00"),
            pd.Timestamp("2026-01-07 13:59:00+00:00"),
            pd.Timestamp("2026-01-08 13:59:00+00:00"),
            pd.Timestamp("2026-01-09 11:34:00+00:00"),  # 13:34 Asia/Jerusalem
        ],
        name="market_close",
    )

    assert_series_equal(actual["market_close"], expected)


def test_tase_2026_high_holidays():
    # Rosh Hashanah eve (Fri Sep 11), Fri Sep 18 before Yom Kippur eve on
    # Sunday, Yom Kippur (Mon Sep 21), Sukkot eve (Fri Sep 25)
    actual = mcal.get_calendar("TASE").schedule("2026-09-07", "2026-09-28").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2026-09-07"),
            pd.Timestamp("2026-09-08"),
            pd.Timestamp("2026-09-09"),
            pd.Timestamp("2026-09-10"),
            pd.Timestamp("2026-09-14"),
            pd.Timestamp("2026-09-15"),
            pd.Timestamp("2026-09-16"),
            pd.Timestamp("2026-09-17"),
            pd.Timestamp("2026-09-22"),
            pd.Timestamp("2026-09-23"),
            pd.Timestamp("2026-09-24"),
            pd.Timestamp("2026-09-28"),
        ]
    )

    assert_index_equal(actual, expected)


def test_tase_2026_passover():
    # Passover eve/first day (Apr 1-2), seventh day eve/day (Apr 7-8)
    actual = mcal.get_calendar("TASE").schedule("2026-03-30", "2026-04-10").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2026-03-30"),
            pd.Timestamp("2026-03-31"),
            pd.Timestamp("2026-04-03"),  # Fri, Passover interim day
            pd.Timestamp("2026-04-06"),
            pd.Timestamp("2026-04-09"),
            pd.Timestamp("2026-04-10"),
        ]
    )

    assert_index_equal(actual, expected)


def test_tase_2027_high_holidays():
    # Rosh Hashanah eve (Fri Oct 1), Fri Oct 8 before Yom Kippur eve on Sunday,
    # Yom Kippur (Mon Oct 11), Sukkot eve (Fri Oct 15), Simchat Torah eve
    # (Fri Oct 22)
    actual = mcal.get_calendar("TASE").schedule("2027-09-27", "2027-10-25").index

    expected = pd.DatetimeIndex(
        [
            pd.Timestamp("2027-09-27"),
            pd.Timestamp("2027-09-28"),
            pd.Timestamp("2027-09-29"),
            pd.Timestamp("2027-09-30"),
            pd.Timestamp("2027-10-04"),
            pd.Timestamp("2027-10-05"),
            pd.Timestamp("2027-10-06"),
            pd.Timestamp("2027-10-07"),
            pd.Timestamp("2027-10-12"),
            pd.Timestamp("2027-10-13"),
            pd.Timestamp("2027-10-14"),
            pd.Timestamp("2027-10-18"),
            pd.Timestamp("2027-10-19"),
            pd.Timestamp("2027-10-20"),
            pd.Timestamp("2027-10-21"),
            pd.Timestamp("2027-10-25"),
        ]
    )

    assert_index_equal(actual, expected)
