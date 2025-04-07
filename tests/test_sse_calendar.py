import datetime

import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.sse import SSEExchangeCalendar
from pandas_market_calendars.holidays.cn import all_holidays

all_holidays = pd.DatetimeIndex(all_holidays)


def test_time_zone():
    assert SSEExchangeCalendar().tz == ZoneInfo("Asia/Shanghai")
    assert SSEExchangeCalendar().name == "SSE"


def test_all_holidays():
    sse_calendar = SSEExchangeCalendar()

    trading_days = sse_calendar.valid_days(all_holidays.min(), all_holidays.max())
    assert not all_holidays.tz_localize("UTC").isin(trading_days).any()

    holidays = [
        "2019-05-03",
        "2020-01-31",
        "2021-02-15",
        "2022-05-04",
    ]
    for date in holidays:
        assert pd.Timestamp(date, tz="UTC") not in trading_days


def test_sse_closes_at_lunch():
    sse_calendar = SSEExchangeCalendar()
    sse_schedule = sse_calendar.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=ZoneInfo("Asia/Shanghai")),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert sse_calendar.open_at_time(
        schedule=sse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert not sse_calendar.open_at_time(
        schedule=sse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 12, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )
