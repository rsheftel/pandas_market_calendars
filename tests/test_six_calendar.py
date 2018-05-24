
import pandas as pd
import pytz
from pandas_market_calendars.exchange_calendar_six import SIXExchangeCalendar


def test_time_zone():
    assert SIXExchangeCalendar().tz == pytz.timezone('Europe/Zurich')
    assert SIXExchangeCalendar().name == 'SIX'


def test_2018_holidays():
    # good friday: 2017-04-14
    # May 1st: 2017-05-01
    # christmas (observed): 2017-12-25
    # new years (observed): on a weekend, not rolled forward
    six = SIXExchangeCalendar()
    good_dates = six.valid_days('2018-01-01', '2018-12-31', tz='Europe/Zurich')

    for date in ["2018-05-24", "2018-06-15", "2018-03-23"]:
        assert pd.Timestamp(date, tz='Europe/Berlin') in good_dates
    for date in ["2018-01-01", "2018-01-02", "2018-03-30", "2018-04-02", "2018-05-01", "2018-05-10", "2018-05-21",
                 "2018-08-01", "2018-12-24", "2018-12-25", "2018-12-26", "2018-12-31"]:
        assert pd.Timestamp(date, tz='Europe/Zurich') not in good_dates
