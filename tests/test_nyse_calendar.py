import datetime as dt
import os
from zoneinfo import ZoneInfo

import pandas as pd
import pytest
from zoneinfo import ZoneInfo
from pandas.testing import assert_index_equal, assert_series_equal

from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar


def test_custom_open_close():
    cal = NYSEExchangeCalendar(open_time=dt.time(9), close_time=dt.time(10))
    sched = cal.schedule("2021-08-16", "2021-08-16")
    assert sched.market_open.iat[0] == pd.Timestamp("2021-08-16 13:00:00+00:00")
    assert sched.market_close.iat[0] == pd.Timestamp("2021-08-16 14:00:00+00:00")

    assert NYSEExchangeCalendar.regular_market_times is not cal.regular_market_times


@pytest.mark.parametrize(
    "dates, results",
    [
        (
            ("1984-12-30", "1985-01-03"),
            ["1984-12-31 10:00:00", "1985-01-02 09:30:00", "1985-01-03 09:30:00"],
        ),
        (
            ("1901-12-13", "1901-12-16"),
            ["1901-12-13 10:00:00", "1901-12-14 10:00:00", "1901-12-16 10:00:00"],
        ),
    ],
)
def test_days_at_time_open(dates, results):
    cal = NYSEExchangeCalendar()

    # check if market_open before/after 1985 is correct
    valid = cal.valid_days(*dates)
    at_open = cal.days_at_time(valid, "market_open")

    assert_series_equal(
        at_open,
        pd.Series(
            results, index=pd.DatetimeIndex(results).normalize(), dtype="datetime64[ns]"
        )
        .dt.tz_localize(cal.tz)
        .dt.tz_convert("UTC"),
    )


@pytest.mark.parametrize(
    "dates, results",
    [
        (
            ("1952-09-26", "1952-09-30"),
            ["1952-09-26 15:00:00", "1952-09-29 15:30:00", "1952-09-30 15:30:00"],
        ),
        (
            ("1973-12-28", "1974-01-02"),
            ["1973-12-28 15:30:00", "1973-12-31 15:30:00", "1974-01-02 16:00:00"],
        ),
        (
            ("1952-05-23", "1952-05-26"),
            ["1952-05-23 15:00:00", "1952-05-24 12:00:00", "1952-05-26 15:00:00"],
        ),
        (
            ("1901-12-13", "1901-12-16"),
            ["1901-12-13 15:00:00", "1901-12-14 12:00:00", "1901-12-16 15:00:00"],
        ),
    ],
)
def test_days_at_time_close(dates, results):
    cal = NYSEExchangeCalendar()
    valid = cal.valid_days(*dates)
    at_close = cal.days_at_time(valid, "market_close")

    results = pd.DatetimeIndex(results)
    ix = pd.DatetimeIndex(results.normalize(), freq=None)
    assert_series_equal(at_close, pd.Series(results.tz_localize(cal.tz).tz_convert("UTC"), index=ix))


def test_days_at_time_custom():
    cal = NYSEExchangeCalendar()

    # test all three market_closes
    valid = cal.valid_days("1952-09-26", "1974-01-02")
    at_close = cal.days_at_time(valid, "market_close").dt.tz_convert(cal.tz)

    assert at_close.iat[0] == pd.Timestamp("1952-09-26 15:00:00").tz_localize(cal.tz)
    assert at_close.iat[1] == pd.Timestamp("1952-09-29 15:30:00").tz_localize(cal.tz)
    assert at_close.iat[-2] == pd.Timestamp("1973-12-31 15:30:00").tz_localize(cal.tz)
    assert at_close.iat[-1] == pd.Timestamp("1974-01-02 16:00:00").tz_localize(cal.tz)

    # check if chosen time is kept
    cal = NYSEExchangeCalendar(close_time=dt.time(10))
    at_close = cal.days_at_time(cal.valid_days("1901-12-13", "1901-12-16"), "market_close")

    results = pd.DatetimeIndex(["1901-12-13 10:00:00", "1901-12-14 10:00:00", "1901-12-16 10:00:00"])
    assert_series_equal(
        at_close,
        pd.Series(results.tz_localize(cal.tz).tz_convert("UTC"), index=results.normalize()),
    )

    # check if chosen time is kept
    cal = NYSEExchangeCalendar(open_time=dt.time(9))
    at_open = cal.days_at_time(cal.valid_days("1901-12-13", "1901-12-16"), "market_open")

    results = pd.DatetimeIndex(["1901-12-13 09:00:00", "1901-12-14 09:00:00", "1901-12-16 09:00:00"])
    assert_series_equal(
        at_open,
        pd.Series(results.tz_localize(cal.tz).tz_convert("UTC"), index=results.normalize()),
    )


def test_valid_days():
    cal = NYSEExchangeCalendar()

    assert cal.valid_days("1999-01-01", "2014-01-01") is not None
    # used to raise an error because tz= None
    assert cal.valid_days("1999-01-01", "2014-01-01", tz=None) is not None

    assert cal.special_dates("market_close", "1999-01-01", "2014-01-01", False) is not None
    # calls valid_days internally
    assert cal.special_dates("market_close", "1999-01-01", "2014-01-01", True) is not None

    start, end = "2000-01-01", "2000-01-30"
    valid = cal.valid_days(start, end, tz="UTC").tz_localize(None)
    for tz in ("America/New_York", "Europe/Berlin", None):
        assert (valid.tz_localize(tz) == cal.valid_days(start, end, tz=tz)).all()

    # test with dates with timezones attached
    start = pd.Timestamp("2000-01-01", tz="America/New_York")
    end = pd.Timestamp("2000-01-30", tz="America/New_York")
    valid_w_tz = cal.valid_days(start, end, tz="UTC").tz_localize(None)
    assert_index_equal(valid, valid_w_tz)


def test_valid_days_tz_aware():
    calendar = NYSEExchangeCalendar()
    data_date = dt.datetime.strptime("20250121", "%Y%m%d").astimezone(ZoneInfo("UTC"))
    actual = calendar.valid_days(data_date, data_date + dt.timedelta(days=7), tz="UTC")
    expected = pd.bdate_range("2025-01-21", periods=6, tz="UTC")
    assert_index_equal(actual, expected)


def test_time_zone():
    assert NYSEExchangeCalendar().tz == ZoneInfo("America/New_York")
    assert NYSEExchangeCalendar().name == "NYSE"


def test_open_time_tz():
    nyse = NYSEExchangeCalendar()
    assert nyse.open_time.tzinfo == nyse.tz


def test_close_time_tz():
    nyse = NYSEExchangeCalendar()
    assert nyse.close_time.tzinfo == nyse.tz


def test_2012():
    nyse = NYSEExchangeCalendar()
    # holidays we expect:
    holidays_2012 = [
        pd.Timestamp("2012-01-02", tz="UTC"),
        pd.Timestamp("2012-01-16", tz="UTC"),
        pd.Timestamp("2012-02-20", tz="UTC"),
        pd.Timestamp("2012-04-06", tz="UTC"),
        pd.Timestamp("2012-05-28", tz="UTC"),
        pd.Timestamp("2012-07-04", tz="UTC"),
        pd.Timestamp("2012-09-03", tz="UTC"),
        pd.Timestamp("2012-11-22", tz="UTC"),
        pd.Timestamp("2012-12-25", tz="UTC"),
    ]

    for session_label in holidays_2012:
        assert session_label not in nyse.valid_days("2012-01-01", "2012-12-31")

    # early closes we expect:
    early_closes_2012 = [
        pd.Timestamp("2012-07-03"),
        pd.Timestamp("2012-11-23"),
        pd.Timestamp("2012-12-24"),
    ]

    expected = nyse.early_closes(nyse.schedule("2012-01-01", "2012-12-31"))
    assert len(expected) == 3
    for early_close_session_label in early_closes_2012:
        assert early_close_session_label in expected.index


def test_special_holidays():
    # 9/11
    # Sept 11, 12, 13, 14 2001
    nyse = NYSEExchangeCalendar()
    good_dates = nyse.valid_days("1985-01-01", "2016-12-31")
    assert pd.Timestamp("9/11/2001", tz="UTC") not in good_dates
    assert pd.Timestamp("9/12/2001", tz="UTC") not in good_dates
    assert pd.Timestamp("9/13/2001", tz="UTC") not in good_dates
    assert pd.Timestamp("9/14/2001", tz="UTC") not in good_dates

    # Hurricane Gloria
    # Sept 27, 1985
    assert pd.Timestamp("9/27/1985", tz="UTC") not in good_dates

    # Hurricane Sandy
    # Oct 29, 30 2012
    assert pd.Timestamp("10/29/2012", tz="UTC") not in good_dates
    assert pd.Timestamp("10/30/2012", tz="UTC") not in good_dates

    # various national days of mourning
    # Gerald Ford - 1/2/2007
    assert pd.Timestamp("1/2/2007", tz="UTC") not in good_dates

    # Ronald Reagan - 6/11/2004
    assert pd.Timestamp("6/11/2004", tz="UTC") not in good_dates

    # Richard Nixon - 4/27/1994
    assert pd.Timestamp("4/27/1994", tz="UTC") not in good_dates


def test_new_years():
    """
    Check whether the MarketCalendar contains certain dates.
    """
    #     January 2012
    # Su Mo Tu We Th Fr Sa
    #  1  2  3  4  5  6  7
    #  8  9 10 11 12 13 14
    # 15 16 17 18 19 20 21
    # 22 23 24 25 26 27 28
    # 29 30 31

    nyse = NYSEExchangeCalendar()
    good_dates = nyse.valid_days("2001-01-01", "2016-12-31")

    # If New Years falls on a weekend, {0} the Monday after is a holiday.
    day_after_new_years_sunday = pd.Timestamp("2012-01-02", tz="UTC")
    assert day_after_new_years_sunday not in good_dates

    # If New Years falls on a weekend, {0} the Tuesday after is the first trading day.
    first_trading_day_after_new_years_sunday = pd.Timestamp("2012-01-03", tz="UTC")
    assert first_trading_day_after_new_years_sunday in good_dates

    #     January 2013
    # Su Mo Tu We Th Fr Sa
    #        1  2  3  4  5
    #  6  7  8  9 10 11 12
    # 13 14 15 16 17 18 19
    # 20 21 22 23 24 25 26
    # 27 28 29 30 31

    # If New Years falls during the week, e.g. {0}, it is a holiday.
    new_years_day = pd.Timestamp("2013-01-01", tz="UTC")
    assert new_years_day not in good_dates

    # If the day after NYE falls during the week, {0} is the first trading day.
    first_trading_day_after_new_years = pd.Timestamp("2013-01-02", tz="UTC")
    assert first_trading_day_after_new_years in good_dates


def test_thanksgiving():
    """
    Check MarketCalendar Thanksgiving dates.
    """
    #     November 2005
    # Su Mo Tu We Th Fr Sa
    #        1  2  3  4  5
    #  6  7  8  9 10 11 12
    # 13 14 15 16 17 18 19
    # 20 21 22 23 24 25 26
    # 27 28 29 30

    nyse = NYSEExchangeCalendar()
    good_dates = nyse.valid_days("2001-01-01", "2016-12-31")

    # If Nov has 4 Thursdays, {0} Thanksgiving is the last Thursday.
    thanksgiving_with_four_weeks = pd.Timestamp("2005-11-24", tz="UTC")
    assert thanksgiving_with_four_weeks not in good_dates

    #     November 2006
    # Su Mo Tu We Th Fr Sa
    #           1  2  3  4
    #  5  6  7  8  9 10 11
    # 12 13 14 15 16 17 18
    # 19 20 21 22 23 24 25
    # 26 27 28 29 30

    # If Nov has 5 Thursdays, {0} Thanksgiving is not the last week.
    thanksgiving_with_five_weeks = pd.Timestamp("2006-11-23", tz="UTC")
    assert thanksgiving_with_five_weeks not in good_dates

    # If NYE falls on a weekend, {0} the Tuesday after is the first trading day.
    first_trading_day_after_new_years_sunday = pd.Timestamp("2012-01-03", tz="UTC")
    assert first_trading_day_after_new_years_sunday in good_dates


def test_day_after_thanksgiving():
    #    November 2012
    # Su Mo Tu We Th Fr Sa
    #              1  2  3
    #  4  5  6  7  8  9 10
    # 11 12 13 14 15 16 17
    # 18 19 20 21 22 23 24
    # 25 26 27 28 29 30

    nyse = NYSEExchangeCalendar()
    good_dates = nyse.schedule("2001-01-01", "2016-12-31")

    fourth_friday_open = pd.Timestamp("11/23/2012 11:00AM", tz="America/New_York")
    fourth_friday = pd.Timestamp("11/23/2012 3:00PM", tz="America/New_York")
    assert fourth_friday_open > good_dates.loc["2012-11-23", "market_open"]
    assert fourth_friday > good_dates.loc["2012-11-23", "market_close"]

    #    November 2013
    # Su Mo Tu We Th Fr Sa
    #                 1  2
    #  3  4  5  6  7  8  9
    # 10 11 12 13 14 15 16
    # 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30

    fifth_friday_open = pd.Timestamp("11/29/2013 11:00AM", tz="America/New_York")
    fifth_friday = pd.Timestamp("11/29/2013 3:00PM", tz="America/New_York")
    assert fifth_friday_open > good_dates.loc["2012-11-23", "market_open"]
    assert fifth_friday > good_dates.loc["2012-11-23", "market_close"]


def test_early_close_independence_day_thursday():
    """
    Prior to 2013, the market closed early the Friday after an Independence Day on Thursday.
    Since and including 2013, the early close is on Wednesday.
    """
    #      July 2002
    # Su Mo Tu We Th Fr Sa
    #     1  2  3  4  5  6
    #  7  8  9 10 11 12 13
    # 14 15 16 17 18 19 20
    # 21 22 23 24 25 26 27
    # 28 29 30 31

    nyse = NYSEExchangeCalendar()
    schedule = nyse.schedule("2001-01-01", "2019-12-31")

    wednesday_before = pd.Timestamp("7/3/2002 3:00PM", tz="America/New_York")
    friday_after_open = pd.Timestamp("7/5/2002 11:00AM", tz="America/New_York")
    friday_after = pd.Timestamp("7/5/2002 3:00PM", tz="America/New_York")
    assert nyse.open_at_time(schedule, wednesday_before) is True
    assert nyse.open_at_time(schedule, friday_after_open) is True
    assert nyse.open_at_time(schedule, friday_after) is False

    #      July 2013
    # Su Mo Tu We Th Fr Sa
    #     1  2  3  4  5  6
    #  7  8  9 10 11 12 13
    # 14 15 16 17 18 19 20
    # 21 22 23 24 25 26 27
    # 28 29 30 31
    wednesday_before = pd.Timestamp("7/3/2013 3:00PM", tz="America/New_York")
    friday_after_open = pd.Timestamp("7/5/2013 11:00AM", tz="America/New_York")
    friday_after = pd.Timestamp("7/5/2013 3:00PM", tz="America/New_York")
    assert nyse.open_at_time(schedule, wednesday_before) is False
    assert nyse.open_at_time(schedule, friday_after_open) is True
    assert nyse.open_at_time(schedule, friday_after) is True

    #      July 2019
    # Su Mo Tu We Th Fr Sa
    #     1  2  3  4  5  6
    #  7  8  9 10 11 12 13
    # 14 15 16 17 18 19 20
    # 21 22 23 24 25 26 27
    # 28 29 30 31
    wednesday_before = pd.Timestamp("7/3/2019 3:00PM", tz="America/New_York")
    friday_after_open = pd.Timestamp("7/5/2019 11:00AM", tz="America/New_York")
    friday_after = pd.Timestamp("7/5/2019 3:00PM", tz="America/New_York")
    assert nyse.open_at_time(schedule, wednesday_before) is False
    assert nyse.open_at_time(schedule, friday_after_open) is True
    assert nyse.open_at_time(schedule, friday_after) is True


def test_all_full_day_holidays_since_1928(request):
    """
    Perform a full comparison of all known full day NYSE holidays since 1928/01/01 and
    make sure that it matches.
    """
    # get the expected dates from the csv file
    expected = pd.read_csv(
        os.path.join(request.fspath.dirname, "data", "nyse_all_full_day_holidays_since_1928.csv"),
        index_col=0,
        parse_dates=True,
        header=None,
    ).index
    expected.name = None

    # calculated expected going direct to the underlying regular and ad_hoc calendars
    nyse = NYSEExchangeCalendar()
    actual = pd.DatetimeIndex(nyse.adhoc_holidays).tz_convert(None).sort_values()
    slice_locs = actual.slice_locs(expected[0], expected[-1])
    actual = actual[slice_locs[0] : slice_locs[1]]
    actual = actual.append(nyse.regular_holidays.holidays(expected[0], expected[-1]))
    actual = actual.sort_values().unique()
    assert_index_equal(expected, actual)

    # using the holidays method
    actual = pd.DatetimeIndex(nyse.holidays().holidays, dtype="datetime64[ns]").unique()
    slice_locs = actual.slice_locs(expected[0], expected[-1])
    actual = actual[slice_locs[0] : slice_locs[1]]
    assert_index_equal(expected, actual)


def test_special_early_close_is_not_trading_day():
    """
    Performs a test for generating a schedule when a date that is a special early close is also an adhoc holiday so
    that the process ignores the early close for the missing date.
    """

    nyse = NYSEExchangeCalendar()
    # 1956-12-24 is a full day holiday and also will show as early close
    actual = nyse.schedule("1956-12-20", "1956-12-30")
    dates = [pd.Timestamp("1956-12-" + x) for x in ["20", "21", "26", "27", "28"]]
    expected = pd.DatetimeIndex(dates)
    assert_index_equal(actual.index, expected)


def test_juneteenth():
    nyse = NYSEExchangeCalendar()
    good_dates = nyse.valid_days("2020-01-01", "2023-12-31")
    # test <2021 no holiday
    assert pd.Timestamp("6/19/2020", tz="UTC") in good_dates
    assert pd.Timestamp("6/18/2021", tz="UTC") in good_dates
    assert pd.Timestamp("6/21/2021", tz="UTC") in good_dates

    # test 2022-2023
    assert pd.Timestamp("6/20/2022", tz="UTC") not in good_dates
    assert pd.Timestamp("6/19/2023", tz="UTC") not in good_dates


if __name__ == "__main__":
    print("runing open")
    test_days_at_time_open()
    print("running close")
    test_days_at_time_close()

    # for ref, obj in locals().copy().items():
    #     if ref.startswith("test_"):
    #         print("running: ", ref)
    #         obj()
#
