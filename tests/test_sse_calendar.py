import datetime

import pandas as pd
import pytz

from pandas_market_calendars.exchange_calendar_sse import SSEExchangeCalendar
from pandas_market_calendars.holidays_cn import all_holidays


def test_time_zone():
    assert SSEExchangeCalendar().tz == pytz.timezone('Asia/Shanghai')
    assert SSEExchangeCalendar().name == 'SSE'


def test_all_holidays():
    sse_calendar = SSEExchangeCalendar()

    trading_days = sse_calendar.valid_days(pd.Timestamp('2004-01-01'), pd.Timestamp('2020-12-31'))
    for session_label in all_holidays:
        assert session_label not in trading_days


def test_sse_closes_at_lunch():
    sse_calendar = SSEExchangeCalendar()
    sse_schedule = sse_calendar.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=pytz.timezone('Asia/Shanghai')),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=pytz.timezone('Asia/Shanghai'))
    )

    assert SSEExchangeCalendar.open_at_time(
        schedule=sse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    )

    assert not SSEExchangeCalendar.open_at_time(
        schedule=sse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 12, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
    )
