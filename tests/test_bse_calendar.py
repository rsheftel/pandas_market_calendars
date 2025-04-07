import datetime

import pandas as pd
import pytest
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.bse import BSEExchangeCalendar, BSEClosedDay


def test_time_zone():
    assert BSEExchangeCalendar().tz == ZoneInfo("Asia/Calcutta")
    assert BSEExchangeCalendar().name == "BSE"


def test_holidays():
    bse_calendar = BSEExchangeCalendar()

    trading_days = bse_calendar.valid_days(
        pd.Timestamp("2004-01-01"), pd.Timestamp("2018-12-31")
    )
    for session_label in BSEClosedDay:
        assert session_label not in trading_days


def test_open_close_time():
    bse_calendar = BSEExchangeCalendar()
    india_time_zone = ZoneInfo("Asia/Calcutta")

    bse_schedule = bse_calendar.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=india_time_zone),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=india_time_zone),
    )

    assert bse_calendar.open_at_time(
        schedule=bse_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=india_time_zone),
    )

    with pytest.raises(ValueError):
        bse_calendar.open_at_time(
            schedule=bse_schedule,
            timestamp=datetime.datetime(2015, 1, 9, 12, 0, tzinfo=india_time_zone),
        )
