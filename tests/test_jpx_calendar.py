import datetime

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


def test_jpx_closes_at_lunch():
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=pytz.timezone('Asia/Tokyo')),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=pytz.timezone('Asia/Tokyo'))
    )

    assert JPXExchangeCalendar.open_at_time(
        schedule=jpx_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=pytz.timezone('Asia/Tokyo'))
    )

    assert not JPXExchangeCalendar.open_at_time(
            schedule=jpx_schedule,
            timestamp=datetime.datetime(2015, 1, 14, 12, 0, tzinfo=pytz.timezone('Asia/Tokyo'))
        )
