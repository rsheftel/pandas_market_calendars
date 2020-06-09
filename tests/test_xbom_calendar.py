import datetime

import pandas as pd
import pytz

from pandas_market_calendars.exchange_calendar_xbom import XBOMExchangeCalendar, XBOMClosedDay


def test_time_zone():
    assert XBOMExchangeCalendar().tz == pytz.timezone('Asia/Calcutta')
    assert XBOMExchangeCalendar().name == 'XBOM'


def test_holidays():
    xbom_calendar = XBOMExchangeCalendar()

    trading_days = xbom_calendar.valid_days(pd.Timestamp('2004-01-01'), pd.Timestamp('2018-12-31'))
    for session_label in XBOMClosedDay:
        assert session_label not in trading_days


def test_open_close_time():
    xbom_calendar = XBOMExchangeCalendar()
    indiaTimeZone = pytz.timezone('Asia/Calcutta')

    xbom_schedule = xbom_calendar.schedule(
        start_date=indiaTimeZone.localize(datetime.datetime(2015, 1, 14)),
        end_date=indiaTimeZone.localize(datetime.datetime(2015, 1, 16))
    )

    assert XBOMExchangeCalendar.open_at_time(
        schedule=xbom_schedule,
        timestamp=indiaTimeZone.localize(datetime.datetime(2015, 1, 14, 11, 0))
    )

    assert not XBOMExchangeCalendar.open_at_time(
        schedule=xbom_schedule,
        timestamp=indiaTimeZone.localize(datetime.datetime(2015, 1, 9, 12, 0))
    )
