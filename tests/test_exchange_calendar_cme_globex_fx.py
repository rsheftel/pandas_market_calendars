import datetime as dt

import pandas as pd
import pytz

from pandas_market_calendars.exchange_calendar_cme_globex_fx import CMECurrencyExchangeCalendar


def test_time_zone():
    assert CMECurrencyExchangeCalendar().tz == pytz.timezone('America/Chicago')
    assert CMECurrencyExchangeCalendar().name == 'CME_Currency'


def test_sunday_opens():
    cme = CMECurrencyExchangeCalendar()
    schedule = cme.schedule('2020-01-01', '2020-01-31', tz='America/New_York')
    assert pd.Timestamp('2020-01-12 18:00:00', tz='America/New_York') == schedule.loc['2020-01-13', 'market_open']


def test_2022_holidays():
    cme = CMECurrencyExchangeCalendar()
    good_dates = cme.valid_days('2022-01-01', '2023-01-10')
    # Closed holidays
    # Good Friday 2022-04-15
    # Christmas (observed): 2022-12-26
    # New Years Day (obscerved) 2023-01-02
    for holiday_date in ["2022-04-15", "2022-12-26", "2023-01-02"]:
        assert pd.Timestamp(holiday_date, tz='UTC') not in good_dates

    # Holidays that currencies are open but many other markets are not
    # Independence day 2022-07-04
    # Labour day 2022-09-05
    # Thanksgiving Thursday 2022-11-24
    for not_holiday_date in ["2022-07-04", "2022-09-05", "2022-11-24"]:
        assert pd.Timestamp(not_holiday_date, tz='UTC') in good_dates


def test_2022_early_closes():
    cme = CMECurrencyExchangeCalendar()
    schedule = cme.schedule('2022-01-01', '2022-12-31')
    early_closes = cme.early_closes(schedule).index

    # Thanksgiving Friday 2022-11-25
    for date in ["2022-11-25"]:
        ts = pd.Timestamp(date)
        assert ts in early_closes

        market_close = schedule.loc[ts].market_close
        assert market_close.tz_convert(cme.tz).time() == dt.time(12, 15)
