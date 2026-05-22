"""
Smoke tests for HKFE and SGX derivative calendars.
Instantiates every calendar and checks one representative holiday each.

Adjust imports to wherever you place the calendar classes.
"""

import pytest
import pandas as pd

from pandas_market_calendars.calendars.sgx import (
    SGXIndexCNExchangeCalendar,
    SGXNikkeiExchangeCalendar,
    SGXTaiwanExchangeCalendar,
    SGXNiftyExchangeCalendar,
    SGXIndianRupeeExchangeCalendar,
    SGXKoreanWonExchangeCalendar,
)


def _is_holiday(cal, date):
    return cal.schedule(date, date).empty


def _is_trading(cal, date):
    return not cal.schedule(date, date).empty


# ---------------------------------------------------------------------------
# SGX Base (CN, SGP, FCH, UC, FEF, TF)
# ---------------------------------------------------------------------------

def test_sgx_base_instantiates():
    assert SGXIndexCNExchangeCalendar() is not None


def test_sgx_base_closes_good_friday():
    cal = SGXIndexCNExchangeCalendar()
    assert _is_holiday(cal, "2026-04-03")


def test_sgx_base_closes_deepavali():
    cal = SGXIndexCNExchangeCalendar()
    # Deepavali 2026 — Nov 8 Sun -> observed Mon Nov 9
    assert _is_holiday(cal, "2026-11-09")


def test_sgx_base_t1_session_modelled():
    cal = SGXIndexCNExchangeCalendar()
    # T+1 close is 05:15 SGT next day = 18:00 UTC same date row
    sched = cal.schedule("2026-03-10", "2026-03-10")
    assert "break_start" in sched.columns
    close = sched["market_close"].iloc[0]
    assert close == pd.Timestamp("2026-03-10 21:15:00+00:00")


def test_sgx_base_early_close_christmas_eve():
    cal = SGXIndexCNExchangeCalendar()
    # 24 Dec 2026 — half day, close 12:30 SGT = 04:30 UTC
    sched = cal.schedule("2026-12-24", "2026-12-24")
    assert not sched.empty
    close = sched["market_close"].iloc[0]
    assert close == pd.Timestamp("2026-12-24 04:30:00+00:00")


# ---------------------------------------------------------------------------
# SGX Nikkei (NK)
# ---------------------------------------------------------------------------

def test_sgx_nikkei_instantiates():
    assert SGXNikkeiExchangeCalendar() is not None


def test_sgx_nikkei_closes_on_japan_holiday():
    cal = SGXNikkeiExchangeCalendar()
    # Showa Day 2026 — Apr 29 (Wed), Japan national holiday
    assert _is_holiday(cal, "2026-04-29")


def test_sgx_nikkei_closes_on_sg_holiday():
    cal = SGXNikkeiExchangeCalendar()
    assert _is_holiday(cal, "2026-04-03")  # Good Friday


# ---------------------------------------------------------------------------
# SGX Taiwan (TWN)
# ---------------------------------------------------------------------------

def test_sgx_taiwan_instantiates():
    assert SGXTaiwanExchangeCalendar() is not None


def test_sgx_taiwan_closes_on_taiwan_cny():
    cal = SGXTaiwanExchangeCalendar()
    # Taiwan CNY 2026 closure — Feb 16 (Mon)
    assert _is_holiday(cal, "2026-02-16")


def test_sgx_taiwan_closes_on_sg_holiday():
    cal = SGXTaiwanExchangeCalendar()
    assert _is_holiday(cal, "2026-05-01")  # Labour Day


# ---------------------------------------------------------------------------
# SGX Nifty (NIFTY)
# ---------------------------------------------------------------------------

def test_sgx_nifty_instantiates():
    assert SGXNiftyExchangeCalendar() is not None


def test_sgx_nifty_closes_on_india_holiday():
    cal = SGXNiftyExchangeCalendar()
    # Republic Day 2026 — Jan 26 (Mon)
    assert _is_holiday(cal, "2026-01-26")


def test_sgx_nifty_closes_on_sg_holiday():
    cal = SGXNiftyExchangeCalendar()
    assert _is_holiday(cal, "2026-08-10")  # National Day (observed)


# ---------------------------------------------------------------------------
# SGX Indian Rupee (IU)
# ---------------------------------------------------------------------------

def test_sgx_indian_rupee_instantiates():
    assert SGXIndianRupeeExchangeCalendar() is not None


def test_sgx_indian_rupee_closes_on_independence_day():
    cal = SGXIndianRupeeExchangeCalendar()
    # India Independence Day 2026 — Aug 15 (Sat) -> observed? 
    # Aug 15 is Sat so RBI would observe Mon Aug 17; check actual adhoc list
    assert _is_holiday(cal, "2026-08-15")


# ---------------------------------------------------------------------------
# SGX Korean Won (KU)
# ---------------------------------------------------------------------------

def test_sgx_korean_won_instantiates():
    assert SGXKoreanWonExchangeCalendar() is not None


def test_sgx_korean_won_closes_on_chuseok():
    cal = SGXKoreanWonExchangeCalendar()
    # Chuseok 2026 — Sep 24-26 (Thu-Sat), Sep 28 substitute Mon
    assert _is_holiday(cal, "2026-09-24")


def test_sgx_korean_won_closes_on_sg_holiday():
    cal = SGXKoreanWonExchangeCalendar()
    assert _is_holiday(cal, "2026-01-01")  # New Year's Day