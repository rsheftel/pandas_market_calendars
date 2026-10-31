import pandas as pd

from pandas_market_calendars.calendars.cboe import (
    CBOEEquityOptionsExchangeCalendar,
    CBOEIndexOptionsExchangeCalendar,
    CFEExchangeCalendar,
)


def test_christmas_eve_early_closes() -> None:
    # Cboe holiday schedules: https://www.cboe.com/about/hours/us-options
    # https://www.cboe.com/about/hours/us-futures
    for calendar in (CFEExchangeCalendar, CBOEEquityOptionsExchangeCalendar, CBOEIndexOptionsExchangeCalendar):
        cal = calendar()
        for date in ["2024-12-24", "2025-12-24", "2026-12-24"]:
            schedule = cal.schedule(date, date)
            close = schedule.loc[pd.Timestamp(date), "market_close"]
            minute = 0 if calendar == CBOEEquityOptionsExchangeCalendar else 15
            expected = pd.Timestamp(f"{date} 12:{minute:02d}", tz=cal.tz)
            assert close == expected
            assert list(cal.early_closes(schedule).index) == [pd.Timestamp(date)]


def test_christmas_eve_does_not_create_closed_sessions() -> None:
    for calendar in (CFEExchangeCalendar, CBOEEquityOptionsExchangeCalendar, CBOEIndexOptionsExchangeCalendar):
        cal = calendar()
        for date in ["2021-12-24", "2022-12-24", "2023-12-24"]:
            assert cal.schedule(date, date).empty
        schedule = cal.schedule("2026-12-23", "2026-12-25")
        assert list(schedule.index) == [
            pd.Timestamp("2026-12-23"),
            pd.Timestamp("2026-12-24"),
        ]
        close = schedule.loc[pd.Timestamp("2026-12-23"), "market_close"]
        minute = 0 if calendar == CBOEEquityOptionsExchangeCalendar else 15
        assert close == pd.Timestamp(f"2026-12-23 15:{minute:02d}", tz=cal.tz)
