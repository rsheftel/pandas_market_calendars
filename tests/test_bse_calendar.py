import datetime

import pandas as pd
import pytest
from zoneinfo import ZoneInfo

from pandas_market_calendars import get_calendar
from pandas_market_calendars.calendars.bse import BSEClosedDay, BSEExchangeCalendar, NSEClosedDay, NSEExchangeCalendar


def test_time_zone():
    assert BSEExchangeCalendar().tz == ZoneInfo("Asia/Calcutta")
    assert BSEExchangeCalendar().name == "BSE"
    assert NSEExchangeCalendar().tz == ZoneInfo("Asia/Calcutta")
    assert NSEExchangeCalendar().name == "NSE"


def test_holidays():
    bse_calendar = BSEExchangeCalendar()

    trading_days = bse_calendar.valid_days(pd.Timestamp("1997-01-01"), pd.Timestamp("2026-12-31"))
    for session_label in BSEClosedDay:
        assert session_label not in trading_days

    nse_calendar = NSEExchangeCalendar()
    nse_trading_days = nse_calendar.valid_days(pd.Timestamp("1997-01-01"), pd.Timestamp("2026-12-31"))
    for session_label in NSEClosedDay:
        assert session_label not in nse_trading_days

    assert pd.Timestamp("2024-05-20", tz="UTC") not in bse_calendar.valid_days("2024-05-17", "2024-05-21")
    assert pd.Timestamp("2024-05-20", tz="UTC") not in nse_calendar.valid_days("2024-05-17", "2024-05-21")


def test_bse_and_nse_aliases_are_separate_calendars():
    assert get_calendar("BSE").name == "BSE"
    assert get_calendar("XBOM").name == "BSE"
    assert get_calendar("NSE").name == "NSE"
    assert get_calendar("XNSE").name == "NSE"
    assert get_calendar("XNSE").name != get_calendar("BSE").name

    assert pd.Timestamp("2024-05-20", tz="UTC") not in get_calendar("XBOM").valid_days("2024-05-17", "2024-05-21")
    assert pd.Timestamp("2024-05-20", tz="UTC") not in get_calendar("XNSE").valid_days("2024-05-17", "2024-05-21")


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
