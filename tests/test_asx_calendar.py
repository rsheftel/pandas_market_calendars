import pytz
import pandas as pd

from pandas_market_calendars.exchange_calendar_asx import ASXExchangeCalendar


def test_time_zone():
    assert ASXExchangeCalendar().tz == pytz.timezone('Australia/Sydney')


def test_2019_holidays():
    # 2019/01/28 - Australia Day (additional day)
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days('2019-01-01', '2019-12-31')
    for date in ["2019-01-28"]:
        assert pd.Timestamp(date, tz='UTC') not in good_dates


def test_2021_holidays():
    # 2021/01/26 - Australia Day
    # 2021/12/27 - Christmas (additional day)
    # 2021/12/28 - Boxing Day (additional day)
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days('2021-01-01', '2021-12-31')
    for date in ["2021-01-26", "2021-12-27", "2021-12-28"]:
        assert pd.Timestamp(date, tz='UTC') not in good_dates


def test_2022_holidays():
    # 2022/01/26 - Australia Day
    # 2022/12/25 - Christmas
    # 2022/12/26 - Boxing Day
    asx = ASXExchangeCalendar()
    good_dates = asx.valid_days('2022-01-01', '2022-12-31')
    for date in ["2022-01-26", "2022-12-25", "2022-12-26"]:
        assert pd.Timestamp(date, tz='UTC') not in good_dates
