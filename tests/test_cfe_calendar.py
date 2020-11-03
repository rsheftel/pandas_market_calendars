import pandas as pd

from pandas_market_calendars.exchange_calendar_cfe import CFEExchangeCalendar


def test_open_time_tz():
    cfe = CFEExchangeCalendar()
    assert cfe.open_time.tzinfo == cfe.tz


def test_close_time_tz():
    cfe = CFEExchangeCalendar()
    assert cfe.close_time.tzinfo == cfe.tz


def test_2016_holidays():
    # new years: jan 1
    # mlk: jan 18
    # presidents: feb 15
    # good friday: mar 25
    # mem day: may 30
    # independence day: july 4
    # labor day: sep 5
    # thanksgiving day: nov 24
    # christmas (observed): dec 26
    # new years (observed): jan 2 2017
    cfe = CFEExchangeCalendar()
    good_dates = cfe.valid_days('2016-01-01', '2016-12-31')
    for day in ["2016-01-01", "2016-01-18", "2016-02-15", "2016-05-30", "2016-07-04", "2016-09-05", "2016-11-24",
                "2016-12-26", "2017-01-02"]:
        assert pd.Timestamp(day, tz='UTC') not in good_dates


def test_good_friday_rule():
    # Good friday is a holiday unless Christmas Day or New Years Day is on a Friday
    cfe = CFEExchangeCalendar()
    valid_days = cfe.valid_days('2015-04-01', '2016-04-01')
    for day in ["2015-04-03", "2016-03-25"]:
        assert day in valid_days


def test_2016_early_closes():
    # only early close is day after thanksgiving: nov 25
    cfe = CFEExchangeCalendar()
    schedule = cfe.schedule('2016-01-01', '2016-12-31')

    dt = pd.Timestamp("2016-11-25", tz='UTC')
    assert dt in cfe.early_closes(schedule).index

    market_close = schedule.loc[dt].market_close
    market_close = market_close.tz_convert(cfe.tz)
    assert market_close.hour == 12
    assert market_close.minute == 15


def test_adhoc_holidays():
    # hurricane sandy: oct 29 2012, oct 30 2012
    # national days of mourning:
    # - apr 27 1994
    # - june 11 2004
    # - jan 2 2007
    cfe = CFEExchangeCalendar()
    valid_days = cfe.valid_days('1994-01-01', '2012-12-31')
    for day in ["1994-04-27", "2004-06-11", "2007-01-02", "2012-10-29", "2012-10-30"]:
        print(day)
        assert day not in valid_days
