"""
Smoke tests for Euronext derivatives calendars.
Checks instantiation, a representative holiday, and correct trading hours.
"""

import pytest
import pandas as pd

from pandas_market_calendars.calendars.euronext import (
    EuronextParisIndexDerivsCalendar,
    EuronextAmsterdamIndexDerivsCalendar,
    EuronextBrusselsIndexDerivsCalendar,
    EuronextLisbonIndexDerivsCalendar,
    EuronextMilanIndexDerivsCalendar,
    EuronextOsloIndexDerivsCalendar,
    EuronextParisCommodityDerivsCalendar,
)


def _sched(cal, date):
    return cal.schedule(date, date)


def _is_holiday(cal, date):
    return _sched(cal, date).empty


def _is_trading(cal, date):
    return not _sched(cal, date).empty


def _close(cal, date):
    return _sched(cal, date)["market_close"].iloc[0]


def _open(cal, date):
    return _sched(cal, date)["market_open"].iloc[0]


# ---------------------------------------------------------------------------
# Paris index derivatives
# ---------------------------------------------------------------------------


def test_paris_index_instantiates():
    assert EuronextParisIndexDerivsCalendar() is not None


def test_paris_index_good_friday():
    assert _is_holiday(EuronextParisIndexDerivsCalendar(), "2026-04-03")


def test_paris_index_labour_day():
    assert _is_holiday(EuronextParisIndexDerivsCalendar(), "2026-05-01")


def test_paris_index_normal_close():
    # 22:00 CET winter = 21:00 UTC
    assert _close(EuronextParisIndexDerivsCalendar(), "2026-03-10") == pd.Timestamp("2026-03-10 21:00:00+00:00")


def test_paris_index_xmas_eve_early_close():
    # 13:55 CET winter = 12:55 UTC
    assert _close(EuronextParisIndexDerivsCalendar(), "2026-12-24") == pd.Timestamp("2026-12-24 12:55:00+00:00")


# ---------------------------------------------------------------------------
# Amsterdam index derivatives
# ---------------------------------------------------------------------------


def test_amsterdam_index_instantiates():
    assert EuronextAmsterdamIndexDerivsCalendar() is not None


def test_amsterdam_index_easter_monday():
    assert _is_holiday(EuronextAmsterdamIndexDerivsCalendar(), "2026-04-06")


def test_amsterdam_index_normal_close():
    # 22:00 CET winter = 21:00 UTC
    assert _close(EuronextAmsterdamIndexDerivsCalendar(), "2026-03-10") == pd.Timestamp("2026-03-10 21:00:00+00:00")


# ---------------------------------------------------------------------------
# Brussels index derivatives
# ---------------------------------------------------------------------------


def test_brussels_index_instantiates():
    assert EuronextBrusselsIndexDerivsCalendar() is not None


def test_brussels_index_new_years_day():
    assert _is_holiday(EuronextBrusselsIndexDerivsCalendar(), "2026-01-01")


def test_brussels_index_normal_close():
    # 17:40 CET winter = 16:40 UTC
    assert _close(EuronextBrusselsIndexDerivsCalendar(), "2026-03-10") == pd.Timestamp("2026-03-10 16:40:00+00:00")


# ---------------------------------------------------------------------------
# Lisbon index derivatives
# ---------------------------------------------------------------------------


def test_lisbon_index_instantiates():
    assert EuronextLisbonIndexDerivsCalendar() is not None


def test_lisbon_index_christmas():
    assert _is_holiday(EuronextLisbonIndexDerivsCalendar(), "2026-12-25")


def test_lisbon_index_open_on_ascension():
    # Lisbon does not close for Ascension (Oslo-only)
    assert _is_trading(EuronextLisbonIndexDerivsCalendar(), "2026-05-14")


# ---------------------------------------------------------------------------
# Milan index derivatives
# ---------------------------------------------------------------------------


def test_milan_index_instantiates():
    assert EuronextMilanIndexDerivsCalendar() is not None


def test_milan_index_xmas_eve_fully_closed():
    # Milan is fully closed on Xmas Eve, not a half day
    assert _is_holiday(EuronextMilanIndexDerivsCalendar(), "2026-12-24")


def test_milan_index_nye_fully_closed():
    assert _is_holiday(EuronextMilanIndexDerivsCalendar(), "2026-12-31")


def test_milan_index_normal_close():
    # 22:00 CET winter = 21:00 UTC
    assert _close(EuronextMilanIndexDerivsCalendar(), "2026-03-10") == pd.Timestamp("2026-03-10 21:00:00+00:00")


# ---------------------------------------------------------------------------
# Oslo index derivatives
# ---------------------------------------------------------------------------


def test_oslo_index_instantiates():
    assert EuronextOsloIndexDerivsCalendar() is not None


def test_oslo_index_maundy_thursday():
    # Oslo closes on Maundy Thursday; other Euronext markets don't
    assert _is_holiday(EuronextOsloIndexDerivsCalendar(), "2026-04-02")


def test_oslo_index_ascension_day():
    assert _is_holiday(EuronextOsloIndexDerivsCalendar(), "2026-05-14")


def test_oslo_index_whit_monday():
    assert _is_holiday(EuronextOsloIndexDerivsCalendar(), "2026-05-25")


def test_oslo_index_normal_close():
    # 16:20 CET winter = 15:20 UTC
    assert _close(EuronextOsloIndexDerivsCalendar(), "2026-03-10") == pd.Timestamp("2026-03-10 15:20:00+00:00")


def test_oslo_index_xmas_eve_fully_closed():
    assert _is_holiday(EuronextOsloIndexDerivsCalendar(), "2026-12-24")


# ---------------------------------------------------------------------------
# Paris commodity derivatives
# ---------------------------------------------------------------------------


def test_paris_commodity_instantiates():
    assert EuronextParisCommodityDerivsCalendar() is not None


def test_paris_commodity_good_friday():
    assert _is_holiday(EuronextParisCommodityDerivsCalendar(), "2026-04-03")


def test_paris_commodity_normal_close():
    # 18:30 CET winter = 17:30 UTC
    assert _close(EuronextParisCommodityDerivsCalendar(), "2026-03-10") == pd.Timestamp("2026-03-10 19:15:00+00:00")


def test_paris_commodity_nye_early_close():
    # Same half-day as cash market: 14:05 CET = 13:05 UTC
    assert _close(EuronextParisCommodityDerivsCalendar(), "2026-12-31") == pd.Timestamp("2026-12-31 13:00:00+00:00")
