import datetime

import pandas as pd
import pytz

from pandas_market_calendars.exchange_calendar_jpx import JPXExchangeCalendar


def test_time_zone():
    assert JPXExchangeCalendar().tz == pytz.timezone('Asia/Tokyo')
    assert JPXExchangeCalendar().name == 'JPX'


def test_all_holidays():
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

    valid_days = jpx_calendar.valid_days(pd.Timestamp('2017-01-01'), pd.Timestamp('2017-12-31'))
    for session_label in holidays_2017:
        assert session_label not in valid_days

    # holidays we expect
    holidays_2018 = [
        pd.Timestamp("2018-01-01", tz='UTC'),
        pd.Timestamp("2018-01-02", tz='UTC'),
        pd.Timestamp("2018-01-03", tz='UTC'),
        pd.Timestamp("2018-01-08", tz='UTC'),
        pd.Timestamp("2018-02-12", tz='UTC'),
        pd.Timestamp("2018-03-21", tz='UTC'),
        pd.Timestamp("2018-04-30", tz='UTC'),
        pd.Timestamp("2018-05-03", tz='UTC'),
        pd.Timestamp("2018-05-04", tz='UTC'),
        pd.Timestamp("2018-05-05", tz='UTC'),
        pd.Timestamp("2018-07-16", tz='UTC'),
        pd.Timestamp("2018-08-11", tz='UTC'),
        pd.Timestamp("2018-09-17", tz='UTC'),
        pd.Timestamp("2018-09-24", tz='UTC'),
        pd.Timestamp("2018-10-08", tz='UTC'),
        pd.Timestamp("2018-11-03", tz='UTC'),
        pd.Timestamp("2018-11-23", tz='UTC'),
        pd.Timestamp("2018-12-24", tz='UTC'),
        pd.Timestamp("2018-12-31", tz='UTC'),
    ]

    valid_days = jpx_calendar.valid_days(pd.Timestamp('2018-01-01'), pd.Timestamp('2018-12-31'))
    for session_label in holidays_2018:
        assert session_label not in valid_days

    # holidays we expect
    holidays_2019 = [
        pd.Timestamp("2019-01-01", tz='UTC'),
        pd.Timestamp("2019-01-02", tz='UTC'),
        pd.Timestamp("2019-01-03", tz='UTC'),
        pd.Timestamp("2019-01-14", tz='UTC'),
        pd.Timestamp("2019-02-11", tz='UTC'),
        pd.Timestamp("2019-03-21", tz='UTC'),
        pd.Timestamp("2019-04-29", tz='UTC'),
        pd.Timestamp("2019-04-30", tz='UTC'),
        pd.Timestamp("2019-05-01", tz='UTC'),
        pd.Timestamp("2019-05-02", tz='UTC'),
        pd.Timestamp("2019-05-03", tz='UTC'),
        pd.Timestamp("2019-05-04", tz='UTC'),
        pd.Timestamp("2019-05-06", tz='UTC'),
        pd.Timestamp("2019-07-15", tz='UTC'),
        pd.Timestamp("2019-08-12", tz='UTC'),
        pd.Timestamp("2019-09-16", tz='UTC'),
        pd.Timestamp("2019-09-23", tz='UTC'),
        pd.Timestamp("2019-10-14", tz='UTC'),
        pd.Timestamp("2019-11-04", tz='UTC'),
        pd.Timestamp("2019-11-23", tz='UTC'),
        pd.Timestamp("2019-12-23", tz='UTC'),
        pd.Timestamp("2019-12-31", tz='UTC'),
    ]

    valid_days = jpx_calendar.valid_days(pd.Timestamp('2019-01-01'), pd.Timestamp('2019-12-31'))
    for session_label in holidays_2019:
        assert session_label not in valid_days


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


def test_jpx_correctly_counts_jpx_autumn_equinox():
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(start_date='2016-09-01', end_date='2019-09-30')
    assert pd.Timestamp('2016-09-22') not in jpx_schedule.index
    assert pd.Timestamp('2016-09-23') in jpx_schedule.index

    assert pd.Timestamp('2017-09-23') not in jpx_schedule.index  # EQUINOX Saturday
    assert pd.Timestamp('2017-09-24') not in jpx_schedule.index  # Sunday
    assert pd.Timestamp('2017-09-25') in jpx_schedule.index  # Monday

    assert pd.Timestamp('2018-09-22') not in jpx_schedule.index  # Saturday
    assert pd.Timestamp('2018-09-23') not in jpx_schedule.index  # EQUINOX Sunday
    assert pd.Timestamp('2018-09-24') not in jpx_schedule.index  # Equinox OBS

    assert pd.Timestamp('2019-09-22') not in jpx_schedule.index  # Sunday
    assert pd.Timestamp('2019-09-23') not in jpx_schedule.index  # EQUINOX
    assert pd.Timestamp('2019-09-24') in jpx_schedule.index  # Monday


def test_jpx_correctly_counts_jpx_vernal_equinox():
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(start_date='2017-03-01', end_date='2019-09-30')

    assert pd.Timestamp('2017-03-20') not in jpx_schedule.index
    assert pd.Timestamp('2017-03-21') in jpx_schedule.index

    assert pd.Timestamp('2018-03-21') not in jpx_schedule.index

    assert pd.Timestamp('2019-03-21') not in jpx_schedule.index
    assert pd.Timestamp('2019-03-20') in jpx_schedule.index
