
import pandas as pd
import pytz
from pandas_market_calendars.exchange_calendar_nyse import NYSEExchangeCalendar


def time_zone():
    assert NYSEExchangeCalendar().tz == pytz.timezone('America/New_York')
    assert NYSEExchangeCalendar().name == 'NYSE'


def test_2012():
    nyse = NYSEExchangeCalendar()
    # holidays we expect:
    holidays_2012 = [
        pd.Timestamp("2012-01-02", tz='UTC'),
        pd.Timestamp("2012-01-16", tz='UTC'),
        pd.Timestamp("2012-02-20", tz='UTC'),
        pd.Timestamp("2012-04-06", tz='UTC'),
        pd.Timestamp("2012-05-28", tz='UTC'),
        pd.Timestamp("2012-07-04", tz='UTC'),
        pd.Timestamp("2012-09-03", tz='UTC'),
        pd.Timestamp("2012-11-22", tz='UTC'),
        pd.Timestamp("2012-12-25", tz='UTC')
    ]

    for session_label in holidays_2012:
        assert session_label not in nyse.valid_days('2012-01-01', '2012-12-31')

    # early closes we expect:
    early_closes_2012 = [
        pd.Timestamp("2012-07-03", tz='UTC'),
        pd.Timestamp("2012-11-23", tz='UTC'),
        pd.Timestamp("2012-12-24", tz='UTC')
    ]

    expected = nyse.early_closes(nyse.schedule('2012-01-01', '2012-12-31'))
    assert len(expected) == 3
    for early_close_session_label in early_closes_2012:
        assert early_close_session_label in expected.index


def test_special_holidays():
    # 9/11
    # Sept 11, 12, 13, 14 2001
    nyse = NYSEExchangeCalendar()
    good_dates = nyse.valid_days('2001-01-01', '2016-12-31')
    assert pd.Timestamp("9/11/2001") not in good_dates
    assert pd.Timestamp("9/12/2001") not in good_dates
    assert pd.Timestamp("9/13/2001") not in good_dates
    assert pd.Timestamp("9/14/2001") not in good_dates

    # Hurricane Sandy
    # Oct 29, 30 2012
    assert pd.Timestamp("10/29/2012") not in good_dates
    assert pd.Timestamp("10/30/2012") not in good_dates

    # various national days of mourning
    # Gerald Ford - 1/2/2007
    assert pd.Timestamp("1/2/2007") not in good_dates

    # Ronald Reagan - 6/11/2004
    assert pd.Timestamp("6/11/2004") not in good_dates

    # Richard Nixon - 4/27/1994
    assert pd.Timestamp("4/27/1994") not in good_dates


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
    good_dates = nyse.valid_days('2001-01-01', '2016-12-31')

    # If New Years falls on a weekend, {0} the Monday after is a holiday.
    day_after_new_years_sunday = pd.Timestamp("2012-01-02", tz='UTC')
    assert day_after_new_years_sunday not in good_dates

    # If New Years falls on a weekend, {0} the Tuesday after is the first trading day.
    first_trading_day_after_new_years_sunday = pd.Timestamp("2012-01-03", tz='UTC')
    assert first_trading_day_after_new_years_sunday in good_dates

    #     January 2013
    # Su Mo Tu We Th Fr Sa
    #        1  2  3  4  5
    #  6  7  8  9 10 11 12
    # 13 14 15 16 17 18 19
    # 20 21 22 23 24 25 26
    # 27 28 29 30 31

    # If New Years falls during the week, e.g. {0}, it is a holiday.
    new_years_day = pd.Timestamp("2013-01-01", tz='UTC')
    assert new_years_day not in good_dates

    # If the day after NYE falls during the week, {0} is the first trading day.
    first_trading_day_after_new_years = pd.Timestamp("2013-01-02", tz='UTC')
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
    good_dates = nyse.valid_days('2001-01-01', '2016-12-31')

    # If Nov has 4 Thursdays, {0} Thanksgiving is the last Thursday.
    thanksgiving_with_four_weeks = pd.Timestamp("2005-11-24", tz='UTC')
    assert thanksgiving_with_four_weeks not in good_dates

    #     November 2006
    # Su Mo Tu We Th Fr Sa
    #           1  2  3  4
    #  5  6  7  8  9 10 11
    # 12 13 14 15 16 17 18
    # 19 20 21 22 23 24 25
    # 26 27 28 29 30

    # If Nov has 5 Thursdays, {0} Thanksgiving is not the last week.
    thanksgiving_with_five_weeks = pd.Timestamp("2006-11-23", tz='UTC')
    assert thanksgiving_with_five_weeks not in good_dates

    # If NYE falls on a weekend, {0} the Tuesday after is the first trading day.
    first_trading_day_after_new_years_sunday = pd.Timestamp("2012-01-03", tz='UTC')
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
    good_dates = nyse.schedule('2001-01-01', '2016-12-31')

    fourth_friday_open = pd.Timestamp('11/23/2012 11:00AM', tz='EST')
    fourth_friday = pd.Timestamp('11/23/2012 3:00PM', tz='EST')
    assert fourth_friday_open > good_dates.loc['2012-11-23', 'market_open']
    assert fourth_friday > good_dates.loc['2012-11-23', 'market_close']

    #    November 2013
    # Su Mo Tu We Th Fr Sa
    #                 1  2
    #  3  4  5  6  7  8  9
    # 10 11 12 13 14 15 16
    # 17 18 19 20 21 22 23
    # 24 25 26 27 28 29 30

    fifth_friday_open = pd.Timestamp('11/29/2013 11:00AM', tz='EST')
    fifth_friday = pd.Timestamp('11/29/2013 3:00PM', tz='EST')
    assert fifth_friday_open > good_dates.loc['2012-11-23', 'market_open']
    assert fifth_friday > good_dates.loc['2012-11-23', 'market_close']


def test_early_close_independence_day_thursday():
    """
    Until 2013, the market closed early the Friday after an
    Independence Day on Thursday.  Since then, the early close is on
    Wednesday.
    """
    #      July 2002
    # Su Mo Tu We Th Fr Sa
    #     1  2  3  4  5  6
    #  7  8  9 10 11 12 13
    # 14 15 16 17 18 19 20
    # 21 22 23 24 25 26 27
    # 28 29 30 31

    nyse = NYSEExchangeCalendar()
    schedule = nyse.schedule('2001-01-01', '2016-12-31')

    wednesday_before = pd.Timestamp('7/3/2002 3:00PM', tz='EST')
    friday_after_open = pd.Timestamp('7/5/2002 11:00AM', tz='EST')
    friday_after = pd.Timestamp('7/5/2002 3:00PM', tz='EST')
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
    wednesday_before = pd.Timestamp('7/3/2013 3:00PM', tz='EST')
    friday_after_open = pd.Timestamp('7/5/2013 11:00AM', tz='EST')
    friday_after = pd.Timestamp('7/5/2013 3:00PM', tz='EST')
    assert nyse.open_at_time(schedule, wednesday_before) is False
    assert nyse.open_at_time(schedule, friday_after_open) is True
    assert nyse.open_at_time(schedule, friday_after) is True
