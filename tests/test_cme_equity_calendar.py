import pandas as pd
import pytz

from pandas_market_calendars.exchange_calendar_cme import CMEEquityExchangeCalendar


def test_time_zone():
    assert CMEEquityExchangeCalendar().tz == pytz.timezone('America/New_York')
    assert CMEEquityExchangeCalendar().name == 'CME_Equity'


def test_sunday_opens():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule('2020-01-01', '2020-01-31', tz='America/New_York')
    assert pd.Timestamp('2020-01-12 18:00:00', tz='America/New_York') == schedule.at['2020-01-13', 'market_open']
