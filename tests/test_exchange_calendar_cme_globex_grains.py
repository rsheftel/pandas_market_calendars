import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.cme_globex_agriculture import (
    CMEGlobexGrainsAndOilseedsExchangeCalendar,
)


cal = CMEGlobexGrainsAndOilseedsExchangeCalendar()


def test_time_zone():
    assert cal.tz == ZoneInfo("America/Chicago")
    assert cal.name == "CMEGlobex_GrainsAndOilseeds"


def test_x():
    schedule = cal.schedule("2023-01-01", "2023-01-10", tz="America/New_York")

    good_dates = cal.valid_days("2023-01-01", "2023-12-31")

    assert all(d not in good_dates for d in {"2023-01-01", "2023-12-24", "2023-12-25", "2023-12-30", "2023-12-31"})

    assert all(d in good_dates for d in {"2023-01-03", "2023-01-05", "2023-12-26", "2023-12-27", "2023-12-28"})


# The end of the last one-minute TRADES bar of ZC, ZS and ZW: NinjaTrader history for 2015-2022 and
# Interactive Brokers history for 2025.
def test_friday_after_thanksgiving_and_christmas_eve_close_at_1205():
    expected_closes = {
        "2015-11-27": pd.Timestamp("2015-11-27 12:05", tz="America/Chicago"),
        "2022-11-25": pd.Timestamp("2022-11-25 12:05", tz="America/Chicago"),
        "2025-11-28": pd.Timestamp("2025-11-28 12:05", tz="America/Chicago"),
        "2015-12-24": pd.Timestamp("2015-12-24 12:05", tz="America/Chicago"),
        "2020-12-24": pd.Timestamp("2020-12-24 12:05", tz="America/Chicago"),
        "2025-12-24": pd.Timestamp("2025-12-24 12:05", tz="America/Chicago"),
        "2025-12-26": pd.Timestamp("2025-12-26 13:20", tz="America/Chicago"),
    }
    schedule = cal.schedule("2015-11-01", "2025-12-31", tz="America/Chicago")

    for session, expected_close in expected_closes.items():
        assert schedule.at[pd.Timestamp(session), "market_close"] == expected_close, session


def test_no_early_closes_before_2015():
    schedule = cal.schedule("2013-01-01", "2014-12-31")

    assert cal.early_closes(schedule).empty
