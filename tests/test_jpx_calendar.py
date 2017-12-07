import pandas as pd
import pytz
from pandas_market_calendars.exchange_calendar_jpx import JPXExchangeCalendar


def test_time_zone():
    assert JPXExchangeCalendar().tz == pytz.timezone('Asia/Tokyo')
    assert JPXExchangeCalendar().name == 'JPX'


def test_2017_holidays():
    jpx_calendar = JPXExchangeCalendar()

    # holidays we expect
    holidays_2017 = [
        pd.Timestamp("2017-01-01", tz='UTC'),
        pd.Timestamp("2017-01-02", tz='UTC'),
        pd.Timestamp("2017-01-03", tz='UTC'),
        pd.Timestamp("2017-01-09", tz='UTC'),
        pd.Timestamp("2017-02-11", tz='UTC'),
        pd.Timestamp("2017-03-20", tz='UTC'),
        pd.Timestamp("2017-04-29", tz='UTC'),
        pd.Timestamp("2017-05-03", tz='UTC'),
        pd.Timestamp("2017-05-04", tz='UTC'),
        pd.Timestamp("2017-05-05", tz='UTC'),
        pd.Timestamp("2017-07-17", tz='UTC'),
        pd.Timestamp("2017-08-11", tz='UTC'),
        pd.Timestamp("2017-09-23", tz='UTC'),
        pd.Timestamp("2017-10-09", tz='UTC'),
        pd.Timestamp("2017-11-03", tz='UTC'),
        pd.Timestamp("2017-11-23", tz='UTC'),
        pd.Timestamp("2017-12-23", tz='UTC'),
        pd.Timestamp("2017-12-31", tz='UTC'),
    ]

    for session_label in holidays_2017:
        assert session_label not in jpx_calendar.valid_days('2017-01-01', '2017-12-31')
