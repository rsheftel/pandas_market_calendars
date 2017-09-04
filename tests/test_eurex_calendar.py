
import pandas as pd
import pytz
from pandas_market_calendars.exchange_calendar_eurex import EUREXExchangeCalendar


def test_time_zone():
    assert EUREXExchangeCalendar().tz == pytz.timezone('Europe/London')
    assert EUREXExchangeCalendar().name == 'EUREX'


def test_2016_holidays():
    # good friday: 2016-03-25
    # May 1st: 2016-05-02
    # christmas (observed): 2016-12-26
    # new years (observed): 2016-01-02
    eurex = EUREXExchangeCalendar()
    good_dates = eurex.valid_days('2016-01-01', '2016-12-31')
    for date in ["2016-03-25", "2016-05-02", "2016-12-26", "2016-01-02"]:
        assert pd.Timestamp(date, tz='UTC') not in good_dates
