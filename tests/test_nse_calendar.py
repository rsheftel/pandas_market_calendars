import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars import get_calendar
from pandas_market_calendars.calendars.nse import NSEExchangeCalendar
from pandas_market_calendars.holidays.nse import NSEClosedDay


def test_time_zone():
    assert NSEExchangeCalendar().tz == ZoneInfo("Asia/Calcutta")
    assert NSEExchangeCalendar().name == "NSE"
    assert NSEExchangeCalendar().full_name == "National Stock Exchange of India"


def test_aliases():
    assert get_calendar("NSE").name == "NSE"
    assert get_calendar("XNSE").name == "NSE"
    assert get_calendar("XNSE").name != get_calendar("BSE").name


def test_holidays():
    nse_calendar = NSEExchangeCalendar()

    assert len(NSEClosedDay) == 453
    assert len(set(NSEClosedDay)) == 453
    assert all(holiday.dayofweek < 5 for holiday in NSEClosedDay)

    trading_days = nse_calendar.valid_days(
        pd.Timestamp("1996-01-01"), pd.Timestamp("2026-12-31")
    )
    for session_label in NSEClosedDay:
        assert session_label not in trading_days

    # Ad hoc closures: 2024 Mumbai election day and the Ram Mandir ceremony.
    assert pd.Timestamp("2024-05-20", tz="UTC") not in trading_days
    assert pd.Timestamp("2024-01-22", tz="UTC") not in trading_days

    # Weekday Muhurat dates are sessions, not holidays.
    assert pd.Timestamp("2024-11-01", tz="UTC") in trading_days
    assert pd.Timestamp("2022-10-24", tz="UTC") in trading_days


def test_regular_hours_2010_transitions():
    nse_calendar = NSEExchangeCalendar()

    schedule = nse_calendar.schedule("2009-12-31", "2010-10-18")

    # Last 9:55 AM IST open.
    assert schedule.loc["2009-12-31", "market_open"] == pd.Timestamp(
        "2009-12-31 04:25", tz="UTC"
    )
    # 9:00 AM IST open, first and last day.
    assert schedule.loc["2010-01-04", "market_open"] == pd.Timestamp(
        "2010-01-04 03:30", tz="UTC"
    )
    assert schedule.loc["2010-10-15", "market_open"] == pd.Timestamp(
        "2010-10-15 03:30", tz="UTC"
    )
    # 9:15 AM IST open, first day.
    assert schedule.loc["2010-10-18", "market_open"] == pd.Timestamp(
        "2010-10-18 03:45", tz="UTC"
    )

    for market_close in schedule["market_close"]:
        assert market_close.time() == pd.Timestamp("10:00").time()


def test_regular_hours_1990s_eras():
    nse_calendar = NSEExchangeCalendar()

    schedule = nse_calendar.schedule("1997-08-06", "1997-08-14")

    # 9:30 AM - 3:00 PM IST era.
    assert schedule.loc["1997-08-06", "market_open"] == pd.Timestamp(
        "1997-08-06 04:00", tz="UTC"
    )
    assert schedule.loc["1997-08-06", "market_close"] == pd.Timestamp(
        "1997-08-06 09:30", tz="UTC"
    )
    # One-week 9:00 AM - 2:30 PM IST era.
    assert schedule.loc["1997-08-07", "market_open"] == pd.Timestamp(
        "1997-08-07 03:30", tz="UTC"
    )
    assert schedule.loc["1997-08-07", "market_close"] == pd.Timestamp(
        "1997-08-07 09:00", tz="UTC"
    )
    assert schedule.loc["1997-08-14", "market_open"] == pd.Timestamp(
        "1997-08-14 04:00", tz="UTC"
    )

    # 9:55 AM - 3:45 PM IST era.
    schedule = nse_calendar.schedule("1999-01-04", "1999-01-04")
    assert schedule.loc["1999-01-04", "market_open"] == pd.Timestamp(
        "1999-01-04 04:25", tz="UTC"
    )
    assert schedule.loc["1999-01-04", "market_close"] == pd.Timestamp(
        "1999-01-04 10:15", tz="UTC"
    )


def _assert_ist_windows(expected_windows):
    nse_calendar = NSEExchangeCalendar()
    for date, (open_ist, close_ist) in expected_windows.items():
        schedule = nse_calendar.schedule(date, date)
        assert schedule.loc[date, "market_open"] == pd.Timestamp(
            f"{date} {open_ist}", tz="Asia/Calcutta"
        )
        assert schedule.loc[date, "market_close"] == pd.Timestamp(
            f"{date} {close_ist}", tz="Asia/Calcutta"
        )


def test_regular_hours_every_era():
    # One trading day on each side of every regular-hours cutover.
    _assert_ist_windows(
        {
            "1997-01-07": ("10:00", "15:30"),
            "1997-07-28": ("10:00", "15:30"),
            "1997-07-30": ("09:30", "15:00"),
            "1997-08-07": ("09:00", "14:30"),
            "1997-08-14": ("09:30", "15:00"),
            "1997-09-26": ("09:30", "15:00"),
            "1997-09-29": ("09:30", "15:30"),
            "1997-10-09": ("09:30", "15:30"),
            "1997-10-10": ("09:30", "16:00"),
            "1998-05-15": ("09:30", "16:00"),
            "1998-05-18": ("09:30", "15:30"),
            "1998-06-30": ("09:30", "15:30"),
            "1998-07-01": ("10:00", "15:30"),
            "1998-11-17": ("10:00", "15:30"),
            "1998-11-18": ("09:55", "15:45"),
            "1999-06-08": ("09:55", "15:45"),
            "1999-06-09": ("09:55", "15:30"),
        }
    )


def test_muhurat_sessions_1998_2012():
    _assert_ist_windows(
        {
            "1998-10-19": ("17:28", "19:29"),
            "2000-10-26": ("18:30", "19:45"),
            "2001-11-14": ("17:00", "18:15"),
            "2002-11-04": ("17:00", "18:15"),
            "2004-11-12": ("17:30", "18:45"),
            "2005-11-01": ("18:05", "19:20"),
            "2007-11-09": ("18:00", "19:00"),
            "2008-10-28": ("18:15", "19:15"),
            "2010-11-05": ("18:15", "19:15"),
            "2011-10-26": ("16:45", "18:00"),
            "2012-11-13": ("15:45", "17:00"),
        }
    )


def test_muhurat_sessions_2014_2025():
    _assert_ist_windows(
        {
            "2014-10-23": ("18:30", "19:30"),
            "2015-11-11": ("17:45", "18:45"),
            "2017-10-19": ("18:30", "19:30"),
            "2018-11-07": ("17:30", "18:30"),
            "2021-11-04": ("18:15", "19:15"),
            "2022-10-24": ("18:15", "19:15"),
            "2024-11-01": ("18:00", "19:00"),
            "2025-10-21": ("13:45", "14:45"),
        }
    )


def test_special_session_dates_consistent():
    nse_calendar = NSEExchangeCalendar()

    open_dates = {
        date for _, dates in nse_calendar.special_opens_adhoc for date in dates
    }
    close_dates = {
        date for _, dates in nse_calendar.special_closes_adhoc for date in dates
    }

    # Close-only dates keep the regular open: the 2021-02-24 outage day and
    # the 1996-1999 observed extended/early closes.
    close_only = close_dates - open_dates
    assert "2021-02-24" in close_only
    assert all(date < "1999-07" for date in close_only - {"2021-02-24"})
    assert open_dates < close_dates

    holiday_dates = {holiday.strftime("%Y-%m-%d") for holiday in NSEClosedDay}
    assert not close_dates & holiday_dates


def test_muhurat_weekend_sessions_are_not_supported():
    # Weekend Muhurat sessions (e.g. Sunday 2023-11-12) are a known limitation.
    nse_calendar = NSEExchangeCalendar()

    assert nse_calendar.schedule("2023-11-11", "2023-11-12").empty


def test_2021_outage_interruption():
    nse_calendar = NSEExchangeCalendar()

    schedule = nse_calendar.schedule("2021-02-24", "2021-02-24", interruptions=True)

    assert schedule.loc["2021-02-24", "market_open"] == pd.Timestamp(
        "2021-02-24 03:45", tz="UTC"
    )
    assert schedule.loc["2021-02-24", "interruption_start_1"] == pd.Timestamp(
        "2021-02-24 06:10", tz="UTC"
    )
    assert schedule.loc["2021-02-24", "interruption_end_1"] == pd.Timestamp(
        "2021-02-24 10:15", tz="UTC"
    )
    assert schedule.loc["2021-02-24", "market_close"] == pd.Timestamp(
        "2021-02-24 11:30", tz="UTC"
    )


def test_backward_compatible_imports():
    from pandas_market_calendars.calendars.bse import NSEClosedDay as compat_closed_day
    from pandas_market_calendars.calendars.bse import (
        NSEExchangeCalendar as compat_calendar,
    )

    assert compat_calendar is NSEExchangeCalendar
    assert compat_closed_day is NSEClosedDay
