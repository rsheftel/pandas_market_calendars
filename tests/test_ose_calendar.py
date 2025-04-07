"""
    Currently only 2017, 2018 and 2019 dates are confirmed.

    Dates based on:
    - (not this is for OBX and Equity Derivatives)
    https://www.oslobors.no/obnewsletter/download/1e05ee05a9c1a472da4c715435ff1314/file/file/Bortfallskalender%202017-2019.pdf
    - https://www.oslobors.no/ob_eng/Oslo-Boers/About-Oslo-Boers/Opening-hours
"""

import pandas as pd
import pytest
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.ose import OSEExchangeCalendar

TIMEZONE = ZoneInfo("Europe/Oslo")


def test_time_zone():
    assert OSEExchangeCalendar().tz == ZoneInfo("Europe/Oslo")


def test_name():
    assert OSEExchangeCalendar().name == "OSE"


def test_open_time_tz():
    ose = OSEExchangeCalendar()
    assert ose.open_time.tzinfo == ose.tz


def test_close_time_tz():
    ose = OSEExchangeCalendar()
    assert ose.close_time.tzinfo == ose.tz


def test_2017_calendar():
    ose = OSEExchangeCalendar()
    ose_schedule = ose.schedule(
        start_date=pd.Timestamp("2017-04-11", tz=TIMEZONE),
        end_date=pd.Timestamp("2017-04-13", tz=TIMEZONE),
    )

    regular_holidays_2017 = [
        pd.Timestamp("2017-04-13", tz=TIMEZONE),
        pd.Timestamp("2017-04-14", tz=TIMEZONE),
        pd.Timestamp("2017-04-17", tz=TIMEZONE),
        pd.Timestamp("2017-05-01", tz=TIMEZONE),
        pd.Timestamp("2017-05-17", tz=TIMEZONE),
        pd.Timestamp("2017-05-25", tz=TIMEZONE),
        pd.Timestamp("2017-06-05", tz=TIMEZONE),
        pd.Timestamp("2017-12-25", tz=TIMEZONE),
        pd.Timestamp("2017-12-26", tz=TIMEZONE),
    ]

    half_trading_days_2017 = [pd.Timestamp("2017-04-12", tz=TIMEZONE)]

    valid_market_dates = ose.valid_days("2017-01-01", "2017-12-31", tz=TIMEZONE)

    for closed_market_date in regular_holidays_2017:
        assert closed_market_date not in valid_market_dates

    for half_trading_day in half_trading_days_2017:
        assert half_trading_day in valid_market_dates

    assert ose.open_at_time(
        schedule=ose_schedule, timestamp=pd.Timestamp("2017-04-12 12PM", tz=TIMEZONE)
    )
    with pytest.raises(ValueError):
        ose.open_at_time(schedule=ose_schedule, timestamp=pd.Timestamp("2017-04-12 2PM", tz=TIMEZONE))


def test_2018_calendar():
    ose = OSEExchangeCalendar()
    ose_schedule = ose.schedule(
        start_date=pd.Timestamp("2018-03-27", tz=TIMEZONE),
        end_date=pd.Timestamp("2018-03-29", tz=TIMEZONE),
    )

    regular_holidays_2018 = [
        pd.Timestamp("2018-01-01", tz=TIMEZONE),
        pd.Timestamp("2018-03-29", tz=TIMEZONE),
        pd.Timestamp("2018-03-30", tz=TIMEZONE),
        pd.Timestamp("2018-05-01", tz=TIMEZONE),
        pd.Timestamp("2018-05-10", tz=TIMEZONE),
        pd.Timestamp("2018-05-17", tz=TIMEZONE),
        pd.Timestamp("2018-05-21", tz=TIMEZONE),
        pd.Timestamp("2018-12-24", tz=TIMEZONE),
        pd.Timestamp("2018-12-25", tz=TIMEZONE),
        pd.Timestamp("2018-12-26", tz=TIMEZONE),
        pd.Timestamp("2018-12-31", tz=TIMEZONE),
    ]

    half_trading_days_2018 = [pd.Timestamp("2018-03-28", tz=TIMEZONE)]

    valid_market_dates = ose.valid_days("2018-01-01", "2018-12-31", tz=TIMEZONE)

    for closed_market_date in regular_holidays_2018:
        assert closed_market_date not in valid_market_dates

    for half_trading_day in half_trading_days_2018:
        assert half_trading_day in valid_market_dates

    assert ose.open_at_time(schedule=ose_schedule, timestamp=pd.Timestamp("2018-03-28 12PM", tz=TIMEZONE))
    with pytest.raises(ValueError):
        ose.open_at_time(
            schedule=ose_schedule,
            timestamp=pd.Timestamp("2018-03-28 1:10PM", tz=TIMEZONE),
        )


def test_2019_calendar():
    ose = OSEExchangeCalendar()
    ose_schedule = ose.schedule(
        start_date=pd.Timestamp("2019-04-16", tz=TIMEZONE),
        end_date=pd.Timestamp("2019-04-18", tz=TIMEZONE),
    )

    regular_holidays_2019 = [
        pd.Timestamp("2019-01-01", tz=TIMEZONE),
        pd.Timestamp("2019-04-18", tz=TIMEZONE),
        pd.Timestamp("2019-04-19", tz=TIMEZONE),
        pd.Timestamp("2019-04-22", tz=TIMEZONE),
        pd.Timestamp("2019-05-01", tz=TIMEZONE),
        pd.Timestamp("2019-05-17", tz=TIMEZONE),
        pd.Timestamp("2019-05-30", tz=TIMEZONE),
        pd.Timestamp("2019-06-10", tz=TIMEZONE),
        pd.Timestamp("2019-12-24", tz=TIMEZONE),
        pd.Timestamp("2019-12-25", tz=TIMEZONE),
        pd.Timestamp("2019-12-26", tz=TIMEZONE),
        pd.Timestamp("2019-12-31", tz=TIMEZONE),
    ]

    half_trading_days_2019 = [pd.Timestamp("2019-04-17", tz=TIMEZONE)]

    valid_market_dates = ose.valid_days("2019-01-01", "2019-12-31", tz=TIMEZONE)

    for closed_market_date in regular_holidays_2019:
        assert closed_market_date not in valid_market_dates

    for half_trading_day in half_trading_days_2019:
        assert half_trading_day in valid_market_dates

    assert ose.open_at_time(schedule=ose_schedule, timestamp=pd.Timestamp("2019-04-17 12PM", tz=TIMEZONE))
    with pytest.raises(ValueError):
        ose.open_at_time(
            schedule=ose_schedule,
            timestamp=pd.Timestamp("2019-04-17 1:10PM", tz=TIMEZONE),
        )
