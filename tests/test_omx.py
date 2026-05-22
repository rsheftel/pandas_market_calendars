"""Tests for MEFFIBEXFuturesCalendar and NasdaqStockholmDerivsCalendar."""

import pandas as pd
from pandas_market_calendars.calendars.omx import NasdaqStockholmDerivsCalendar


def _sched(cal, date):
    return cal.schedule(date, date)

def _is_holiday(cal, date):
    return _sched(cal, date).empty

def _close(cal, date):
    return _sched(cal, date)["market_close"].iloc[0]



# ---------------------------------------------------------------------------
# Nasdaq Stockholm OMXS30
# ---------------------------------------------------------------------------

def test_omx_instantiates():
    assert NasdaqStockholmDerivsCalendar() is not None

def test_omx_epiphany_closed():
    assert _is_holiday(NasdaqStockholmDerivsCalendar(), "2026-01-06")

def test_omx_ascension_day_closed():
    assert _is_holiday(NasdaqStockholmDerivsCalendar(), "2026-05-14")

def test_omx_midsummer_eve_closed():
    assert _is_holiday(NasdaqStockholmDerivsCalendar(), "2026-06-19")

def test_omx_christmas_eve_closed():
    assert _is_holiday(NasdaqStockholmDerivsCalendar(), "2026-12-24")

def test_omx_new_years_eve_closed():
    assert _is_holiday(NasdaqStockholmDerivsCalendar(), "2026-12-31")

def test_omx_maundy_thursday_early_close():
    # Open with early close at 13:00 CET = 11:00 UTC (winter)
    assert _close(NasdaqStockholmDerivsCalendar(), "2026-04-02") == pd.Timestamp("2026-04-02 11:00:00+00:00")

def test_omx_normal_hours():
    # CET winter = UTC+1; 09:00 CET = 08:00 UTC, 17:30 CET = 16:30 UTC
    sched = _sched(NasdaqStockholmDerivsCalendar(), "2026-03-10")
    assert sched["market_open"].iloc[0]  == pd.Timestamp("2026-03-10 08:00:00+00:00")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 16:30:00+00:00")