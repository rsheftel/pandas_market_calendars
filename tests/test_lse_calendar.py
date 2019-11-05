import pandas as pd
import pytz

from pandas_market_calendars.exchange_calendar_lse import LSEExchangeCalendar


def test_time_zone():
    assert LSEExchangeCalendar().tz == pytz.timezone('Europe/London')


def test_2012_holidays():
    # 2012/06/04 - Bank Holiday
    # 2012/06/05 - Queen's Diamond Jubilee
    lse = LSEExchangeCalendar()
    good_dates = lse.valid_days('2012-01-01', '2012-12-31')
    for date in ["2012-06-04", "2012-06-05"]:
        assert pd.Timestamp(date, tz='UTC') not in good_dates


def test_2016_holidays():
    # 2016/01/01 - New Years Day (observed on first business day on/after)
    # 2016/03/25 - Good Friday
    # 2016/03/28 - Easter Monday
    # 2016/05/02 - Early May Bank Holiday (first Monday in May)
    # 2016/05/30 - Spring Bank Holiday (last Monday in May)
    # 2016/08/29 - Summer Bank Holiday (last Monday in August)
    # 2016/12/27 - Dec. 27th (Christmas is on a weekend)
    # 2016/12/26 - Boxing Day
    lse = LSEExchangeCalendar()
    good_dates = lse.valid_days('2016-01-01', '2016-12-31')
    for date in ["2016-01-01", "2016-03-25", "2016-03-28", '2016-05-02', '2016-05-30',
                 '2016-08-29', '2016-12-27', '2016-12-26']:
        assert pd.Timestamp(date, tz='UTC') not in good_dates


def test_2016_early_closes():
    # Christmas Eve: 2016-12-23
    # New Year's Eve: 2016-12-30

    lse = LSEExchangeCalendar()
    schedule = lse.schedule('2016-01-01', '2017-12-31')
    early_closes = lse.early_closes(schedule).index

    for date in ["2016-12-23", "2016-12-30", '2017-12-22', '2017-12-29']:
        dt = pd.Timestamp(date, tz='UTC')
        assert dt in early_closes

        market_close = schedule.loc[dt].market_close
        assert market_close.tz_convert(lse.tz).hour == 12
        assert market_close.tz_convert(lse.tz).minute == 30
