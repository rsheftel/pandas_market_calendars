"""
Tests for KRX derivatives calendars.
"""

import pandas as pd
import pytest
import warnings

from pandas_market_calendars.calendars.krx import (
    KRXEquityIndexFuturesCalendar,
    KRXGovernmentBondFuturesCalendar,
    KRXFXFuturesCalendar,
)


def _sched(cal, date):
    return cal.schedule(date, date)


# ---------------------------------------------------------------------------
# Equity Index Futures (KOSPI 200)
# ---------------------------------------------------------------------------

def test_krx_equity_instantiates():
    assert KRXEquityIndexFuturesCalendar() is not None

def test_krx_equity_samil_day_closed():
    assert _sched(KRXEquityIndexFuturesCalendar(), "2026-03-01").empty

def test_krx_equity_chuseok_closed():
    assert _sched(KRXEquityIndexFuturesCalendar(), "2026-09-24").empty

def test_krx_equity_year_end_closed():
    assert _sched(KRXEquityIndexFuturesCalendar(), "2026-12-31").empty

def test_krx_equity_normal_hours():
    # KST = UTC+9, no DST
    sched = _sched(KRXEquityIndexFuturesCalendar(), "2026-03-10")
    assert sched["market_open"].iloc[0]  == pd.Timestamp("2026-03-10 00:00:00+00:00")
    assert sched["break_start"].iloc[0] == pd.Timestamp("2026-03-10 06:45:00+00:00")
    assert sched["break_end"].iloc[0]   == pd.Timestamp("2026-03-10 09:00:00+00:00")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 20:00:00+00:00")


# ---------------------------------------------------------------------------
# Government Bond Futures (KTB)
# ---------------------------------------------------------------------------

def test_krx_bond_instantiates():
    assert KRXGovernmentBondFuturesCalendar() is not None

def test_krx_bond_liberation_day_closed():
    assert _sched(KRXGovernmentBondFuturesCalendar(), "2026-08-15").empty

def test_krx_bond_normal_hours():
    # Same session structure as equity futures
    sched = _sched(KRXGovernmentBondFuturesCalendar(), "2026-03-10")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 20:00:00+00:00")


# ---------------------------------------------------------------------------
# FX Futures (USD/KRW)
# ---------------------------------------------------------------------------

def test_krx_fx_instantiates():
    assert KRXFXFuturesCalendar() is not None

def test_krx_fx_national_foundation_day_closed():
    assert _sched(KRXFXFuturesCalendar(), "2026-10-03").empty

def test_krx_fx_day_session_only():
    # No night session — close is 15:30 KST = 06:30 UTC same day
    sched = _sched(KRXFXFuturesCalendar(), "2026-03-10")
    assert sched["market_open"].iloc[0]  == pd.Timestamp("2026-03-10 00:00:00+00:00")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 06:30:00+00:00")
    assert "break_start" not in sched.columns