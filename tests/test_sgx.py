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
    SGXRubberExchangeCalendar,
    SGXIronOreExchangeCalendar,
    SGXMSCISingaporeExchangeCalendar
)


def _is_holiday(cal, date):
    return cal.schedule(date, date).empty


def _is_trading(cal, date):
    return not cal.schedule(date, date).empty


# ---------------------------------------------------------------------------
# SGX Base (CN, SGP, FCH, UC, FEF, TF)
# ---------------------------------------------------------------------------

def test_sgx_base_instantiates():
    assert (cal := SGXIndexCNExchangeCalendar()) is not None
    cal.name 


def test_sgx_CN_open_good_friday():
    cal = SGXIndexCNExchangeCalendar()
    assert _is_trading(cal, "2026-04-03")


def test_sgx_base_open_deepavali():
    cal = SGXIndexCNExchangeCalendar()
    # Deepavali 2026 — Nov 8 Sun -> observed Mon Nov 9
    assert _is_trading(cal, "2026-11-09")


def test_sgx_base_t1_session_modelled():
    cal = SGXIndexCNExchangeCalendar()
    # T+1 close is 05:15 SGT next day = 18:00 UTC same date row
    sched = cal.schedule("2026-03-10", "2026-03-10")
    assert "break_start" in sched.columns
    close = sched["market_close"].iloc[0]
    assert close == pd.Timestamp("2026-03-10 21:15:00+00:00")



def test_rubber_closes_on_sgx_holiday():
    cal = SGXRubberExchangeCalendar()
    assert _is_holiday(cal, "2026-05-01")  # Labour Day


def test_ironore_closes_on_christmas_holiday():
    cal = SGXIronOreExchangeCalendar()
    assert _is_holiday(cal, "2026-12-25") 


def test_sgx_signapore_non_empty():
    cal = SGXMSCISingaporeExchangeCalendar()
    # Republic Day 2026 — Jan 26 (Mon)
    assert _is_trading(cal, "2026-01-26")


# ---------------------------------------------------------------------------
# SGX Nikkei (NK)
# ---------------------------------------------------------------------------

def test_sgx_nikkei_instantiates():
    assert (cal := SGXNikkeiExchangeCalendar()) is not None
    cal.name


def test_sgx_nikkei_closes_on_ny():
    cal = SGXNikkeiExchangeCalendar()
    assert _is_holiday(cal, "2026-01-01")


def test_sgx_nikkei_open_sg_holiday():
    cal = SGXNikkeiExchangeCalendar()
    assert not _is_holiday(cal, "2026-04-03")  # Good Friday


# ---------------------------------------------------------------------------
# SGX Taiwan (TWN)
# ---------------------------------------------------------------------------

def test_sgx_taiwan_instantiates():
    assert (cal:=SGXTaiwanExchangeCalendar()) is not None
    cal.name


def test_sgx_taiwan_open_on_taiwan_cny():
    cal = SGXTaiwanExchangeCalendar()
    # Taiwan CNY 2026 closure — Feb 16 (Mon)
    assert _is_trading(cal, "2026-02-16")


def test_sgx_taiwan_open_on_sg_holiday():
    cal = SGXTaiwanExchangeCalendar()
    assert _is_trading(cal, "2026-05-01")  # Labour Day


# ---------------------------------------------------------------------------
# SGX Nifty (NIFTY)
# ---------------------------------------------------------------------------

def test_sgx_nifty_instantiates():
    assert (cal := SGXNiftyExchangeCalendar()) is not None
    cal.name


def test_sgx_nifty_closes_on_india_holiday():
    cal = SGXNiftyExchangeCalendar()
    # Republic Day 2026 — Jan 26 (Mon)
    assert _is_holiday(cal, "2026-01-26")


def test_sgx_nifty_open_on_ny():
    cal = SGXNiftyExchangeCalendar()
    assert _is_trading(cal, "2026-01-01")


def test_sgx_nifty_open_on_sg_holiday():
    cal = SGXNiftyExchangeCalendar()
    assert _is_trading(cal, "2026-08-10") 


# ---------------------------------------------------------------------------
# SGX Indian Rupee (IU)
# ---------------------------------------------------------------------------

def test_sgx_indian_rupee_instantiates():
    assert (cal := SGXIndianRupeeExchangeCalendar()) is not None
    cal.name

def test_sgx_indian_rupee_open_on_independence_day():
    cal = SGXIndianRupeeExchangeCalendar()
    # India Independence Day 2026 — Aug 15 (Sat) -> observed? 
    # Aug 15 is Sat so RBI would observe Mon Aug 17; 
    assert not _is_holiday(cal, "2026-08-17")


# ---------------------------------------------------------------------------
# SGX Korean Won (KU)
# ---------------------------------------------------------------------------

def test_sgx_korean_won_instantiates():
    assert (cal := SGXKoreanWonExchangeCalendar()) is not None
    cal.name


def test_sgx_korean_won_open_on_chuseok():
    cal = SGXKoreanWonExchangeCalendar()
    # Chuseok 2026 — Sep 24-26 (Thu-Sat), Sep 28 substitute Mon
    assert not _is_holiday(cal, "2026-09-24")
