"""
Tests for Bursa Malaysia and ICE/Endex market calendars.

Each calendar is tested for:
  - instantiation
  - two regular trading days present in schedule
  - full-closure holidays absent from schedule
  - early-close days present with correct close time (UTC)

All close times are checked in UTC. Offset from local:
  - Europe/London (GMT winter / BST+1 summer)
  - Europe/Amsterdam (CET+1 winter / CEST+2 summer)
  - Asia/Kuala_Lumpur (MYT = UTC+8, no DST)

Early-close times stored by pandas_market_calendars are in UTC.
"""

import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Import all calendars — adjust the import path to wherever you keep them
# ---------------------------------------------------------------------------
from pandas_market_calendars.calendars.iceeu import (
    IFEUEnergyExchangeCalendar,
    IFEUNaturalGasAndEmissionsExchangeCalendar,
    IFEUSoftCommoditiesExchangeCalendar,
    IFEUUKFixedIncomeExchangeCalendar,
    IFEUEuropeanFixedIncomeExchangeCalendar,
    IFEUEquityExchangeCalendar,
    ICEEndexGasPowerExchangeCalendar,
    ICEEndexEmissionsExchangeCalendar,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def assert_is_trading_day(cal, date):
    """Date must appear as a row in the schedule."""
    sched = cal.schedule(date, date)
    assert not sched.empty, f"{cal.name}: expected {date} to be a trading day"


def assert_is_holiday(cal, date):
    """Date must NOT appear in the schedule (full closure)."""
    sched = cal.schedule(date, date)
    assert sched.empty, f"{cal.name}: expected {date} to be a holiday"


def assert_early_close_utc(cal, date, expected_utc_close: str):
    """
    Check that the market_close for `date` in the schedule matches
    `expected_utc_close` (ISO string, e.g. '2026-04-03 18:30:00+00:00').
    """
    sched = cal.schedule(date, date)
    assert not sched.empty, f"{cal.name}: {date} not in schedule (is it a holiday?)"
    actual = sched["market_close"].iloc[0]
    expected = pd.Timestamp(expected_utc_close)
    assert actual == expected, (
        f"{cal.name}: close on {date} expected {expected}, got {actual}"
    )


# ---------------------------------------------------------------------------
# 2. IFEU Energy
#    Normal close: 23:00 London = 23:00 UTC (winter) / 22:00 UTC (summer)
#    Early close C (US holidays): 18:30 London winter = 18:30 UTC
#    Early close Christmas Eve: 19:00 London winter = 19:00 UTC
# ---------------------------------------------------------------------------

@pytest.fixture
def ifeu_energy():
    return IFEUEnergyExchangeCalendar()


def test_ifeu_energy_instantiates(ifeu_energy):
    assert ifeu_energy is not None


def test_ifeu_energy_regular_trading_days(ifeu_energy):
    assert_is_trading_day(ifeu_energy, "2026-03-10")
    assert_is_trading_day(ifeu_energy, "2026-07-14")


def test_ifeu_energy_new_years_day(ifeu_energy):
    assert_is_holiday(ifeu_energy, "2026-01-01")


def test_ifeu_energy_good_friday(ifeu_energy):
    assert_is_holiday(ifeu_energy, "2026-04-03")


def test_ifeu_energy_christmas_day(ifeu_energy):
    assert_is_holiday(ifeu_energy, "2026-12-25")


def test_ifeu_energy_open_easter_monday(ifeu_energy):
    # Energy stays open on Easter Monday
    assert_is_trading_day(ifeu_energy, "2026-04-06")


def test_ifeu_energy_open_may_day(ifeu_energy):
    assert_is_trading_day(ifeu_energy, "2026-05-04")


def test_ifeu_energy_open_boxing_day(ifeu_energy):
    assert_is_trading_day(ifeu_energy, "2026-12-28")


def test_ifeu_energy_early_close_christmas_eve(ifeu_energy):
    # 24 Dec 2026 is Thursday (winter → UTC offset 0)
    # Energy closes 19:00 London = 19:00 UTC
    assert_early_close_utc(ifeu_energy, "2026-12-24", "2026-12-24 19:00:00+00:00")


def test_ifeu_energy_early_close_thanksgiving(ifeu_energy):
    # Thanksgiving 2026 = 26 Nov (Thursday), status C → 18:30 London = 18:30 UTC (winter)
    assert_early_close_utc(ifeu_energy, "2026-11-26", "2026-11-26 18:30:00+00:00")


def test_ifeu_energy_early_close_thanksgiving_friday(ifeu_energy):
    # Thanksgiving Friday 2026 = 27 Nov, status B → 20:00 London = 20:00 UTC (winter)
    assert_early_close_utc(ifeu_energy, "2026-11-27", "2026-11-27 20:00:00+00:00")


def test_ifeu_energy_early_close_independence_day(ifeu_energy):
    # 4 Jul 2026 = Saturday → observed Monday 6 Jul (summer, BST = UTC+1)
    # 18:30 London BST = 17:30 UTC
    assert_early_close_utc(ifeu_energy, "2026-07-06", "2026-07-06 17:30:00+00:00")


def test_ifeu_energy_early_close_new_years_eve(ifeu_energy):
    # 31 Dec 2026 is Thursday (winter → UTC offset 0)
    # Energy closes 20:00 London = 20:00 UTC
    assert_early_close_utc(ifeu_energy, "2026-12-31", "2026-12-31 20:00:00+00:00")


# ---------------------------------------------------------------------------
# 3. IFEU Natural Gas & Emissions
#    Normal close: 17:00 London
#    Early close: 17:00 London on Christmas Eve and New Year's Eve
#    (same as normal — effectively no change in close time for this segment)
# ---------------------------------------------------------------------------

@pytest.fixture
def ifeu_gas():
    return IFEUNaturalGasAndEmissionsExchangeCalendar()


def test_ifeu_gas_instantiates(ifeu_gas):
    assert ifeu_gas is not None


def test_ifeu_gas_regular_trading_days(ifeu_gas):
    assert_is_trading_day(ifeu_gas, "2026-03-10")
    assert_is_trading_day(ifeu_gas, "2026-09-15")


def test_ifeu_gas_good_friday(ifeu_gas):
    assert_is_holiday(ifeu_gas, "2026-04-03")


def test_ifeu_gas_easter_monday(ifeu_gas):
    assert_is_holiday(ifeu_gas, "2026-04-06")


def test_ifeu_gas_may_day(ifeu_gas):
    assert_is_holiday(ifeu_gas, "2026-05-04")


def test_ifeu_gas_spring_bank_holiday(ifeu_gas):
    # Last Monday of May 2026 = 25 May
    assert_is_holiday(ifeu_gas, "2026-05-25")


def test_ifeu_gas_summer_bank_holiday(ifeu_gas):
    # Last Monday of August 2026 = 31 Aug
    assert_is_holiday(ifeu_gas, "2026-08-31")


def test_ifeu_gas_boxing_day(ifeu_gas):
    # 26 Dec 2026 is Saturday → observed Monday 28 Dec
    assert_is_holiday(ifeu_gas, "2026-12-28")


def test_ifeu_gas_open_on_us_holidays(ifeu_gas):
    # Thanksgiving is not a closure for gas/emissions
    assert_is_trading_day(ifeu_gas, "2026-11-26")


# ---------------------------------------------------------------------------
# 4. IFEU Soft Commodities
#    Normal close: 17:30 London
#    Early close Christmas Eve: 12:23 London
# ---------------------------------------------------------------------------

@pytest.fixture
def ifeu_softs():
    return IFEUSoftCommoditiesExchangeCalendar()


def test_ifeu_softs_instantiates(ifeu_softs):
    assert ifeu_softs is not None


def test_ifeu_softs_regular_trading_days(ifeu_softs):
    assert_is_trading_day(ifeu_softs, "2026-02-03")
    assert_is_trading_day(ifeu_softs, "2026-10-20")


def test_ifeu_softs_good_friday(ifeu_softs):
    assert_is_holiday(ifeu_softs, "2026-04-03")


def test_ifeu_softs_easter_monday(ifeu_softs):
    assert_is_holiday(ifeu_softs, "2026-04-06")


def test_ifeu_softs_summer_bank_holiday(ifeu_softs):
    assert_is_holiday(ifeu_softs, "2026-08-31")


def test_ifeu_softs_boxing_day(ifeu_softs):
    assert_is_holiday(ifeu_softs, "2026-12-28")


def test_ifeu_softs_early_close_christmas_eve(ifeu_softs):
    # 24 Dec 2026 winter: 12:23 London = 12:23 UTC
    assert_early_close_utc(ifeu_softs, "2026-12-24", "2026-12-24 12:23:00+00:00")


def test_ifeu_softs_normal_new_years_eve(ifeu_softs):
    # NYE is a normal trading day for softs
    assert_is_trading_day(ifeu_softs, "2026-12-31")


# ---------------------------------------------------------------------------
# 5. IFEU UK Fixed Income (Gilts / SONIA)
#    Normal close: 18:00 London
#    Early close Christmas Eve + NYE: 12:15 London
# ---------------------------------------------------------------------------

@pytest.fixture
def ifeu_gilts():
    return IFEUUKFixedIncomeExchangeCalendar()


def test_ifeu_gilts_instantiates(ifeu_gilts):
    assert ifeu_gilts is not None


def test_ifeu_gilts_regular_trading_days(ifeu_gilts):
    assert_is_trading_day(ifeu_gilts, "2026-03-10")
    assert_is_trading_day(ifeu_gilts, "2026-09-15")


def test_ifeu_gilts_good_friday(ifeu_gilts):
    assert_is_holiday(ifeu_gilts, "2026-04-03")


def test_ifeu_gilts_easter_monday(ifeu_gilts):
    assert_is_holiday(ifeu_gilts, "2026-04-06")


def test_ifeu_gilts_labour_day_1_may(ifeu_gilts):
    # Gilts close on 1 May (continental Labour Day) as well as UK May Day BH
    assert_is_holiday(ifeu_gilts, "2026-05-01")


def test_ifeu_gilts_may_day_bh(ifeu_gilts):
    assert_is_holiday(ifeu_gilts, "2026-05-04")


def test_ifeu_gilts_summer_bank_holiday(ifeu_gilts):
    assert_is_holiday(ifeu_gilts, "2026-08-31")


def test_ifeu_gilts_boxing_day(ifeu_gilts):
    assert_is_holiday(ifeu_gilts, "2026-12-28")


def test_ifeu_gilts_early_close_christmas_eve(ifeu_gilts):
    # 24 Dec 2026 winter: 12:15 London = 12:15 UTC
    assert_early_close_utc(ifeu_gilts, "2026-12-24", "2026-12-24 12:15:00+00:00")


def test_ifeu_gilts_early_close_new_years_eve(ifeu_gilts):
    # 31 Dec 2026 winter: 12:15 London = 12:15 UTC
    assert_early_close_utc(ifeu_gilts, "2026-12-31", "2026-12-31 12:15:00+00:00")


# ---------------------------------------------------------------------------
# 6. IFEU European Fixed Income (Bund / Euribor)
#    Normal close: 21:00 London
#    Full closures: ECB set only (no UK bank holidays)
#    Early close Christmas Eve + NYE: 12:15 London
# ---------------------------------------------------------------------------

@pytest.fixture
def ifeu_eur_fi():
    return IFEUEuropeanFixedIncomeExchangeCalendar()


def test_ifeu_eur_fi_instantiates(ifeu_eur_fi):
    assert ifeu_eur_fi is not None


def test_ifeu_eur_fi_regular_trading_days(ifeu_eur_fi):
    assert_is_trading_day(ifeu_eur_fi, "2026-03-10")
    assert_is_trading_day(ifeu_eur_fi, "2026-09-15")


def test_ifeu_eur_fi_good_friday(ifeu_eur_fi):
    assert_is_holiday(ifeu_eur_fi, "2026-04-03")


def test_ifeu_eur_fi_easter_monday(ifeu_eur_fi):
    assert_is_holiday(ifeu_eur_fi, "2026-04-06")


def test_ifeu_eur_fi_labour_day_1_may(ifeu_eur_fi):
    assert_is_holiday(ifeu_eur_fi, "2026-05-01")


def test_ifeu_eur_fi_christmas_day(ifeu_eur_fi):
    assert_is_holiday(ifeu_eur_fi, "2026-12-25")


def test_ifeu_eur_fi_open_may_day_bh(ifeu_eur_fi):
    # EUR FI does NOT close on UK May Day BH (first Mon of May)
    assert_is_trading_day(ifeu_eur_fi, "2026-05-04")


def test_ifeu_eur_fi_open_summer_bank_holiday(ifeu_eur_fi):
    assert_is_trading_day(ifeu_eur_fi, "2026-08-31")


def test_ifeu_eur_fi_open_boxing_day(ifeu_eur_fi):
    assert_is_trading_day(ifeu_eur_fi, "2026-12-28")


def test_ifeu_eur_fi_early_close_christmas_eve(ifeu_eur_fi):
    # 24 Dec 2026 winter: 12:15 London = 12:15 UTC
    assert_early_close_utc(ifeu_eur_fi, "2026-12-24", "2026-12-24 12:15:00+00:00")


def test_ifeu_eur_fi_early_close_new_years_eve(ifeu_eur_fi):
    assert_early_close_utc(ifeu_eur_fi, "2026-12-31", "2026-12-31 12:15:00+00:00")


# ---------------------------------------------------------------------------
# 7. IFEU Equity (FTSE 100 / 250)
#    Normal close: 21:00 London
#    Early close Christmas Eve + NYE: 12:50 London
# ---------------------------------------------------------------------------

@pytest.fixture
def ifeu_equity():
    return IFEUEquityExchangeCalendar()


def test_ifeu_equity_instantiates(ifeu_equity):
    assert ifeu_equity is not None


def test_ifeu_equity_regular_trading_days(ifeu_equity):
    assert_is_trading_day(ifeu_equity, "2026-03-10")
    assert_is_trading_day(ifeu_equity, "2026-10-20")


def test_ifeu_equity_good_friday(ifeu_equity):
    assert_is_holiday(ifeu_equity, "2026-04-03")


def test_ifeu_equity_easter_monday(ifeu_equity):
    assert_is_holiday(ifeu_equity, "2026-04-06")


def test_ifeu_equity_may_day_bh(ifeu_equity):
    assert_is_holiday(ifeu_equity, "2026-05-04")


def test_ifeu_equity_spring_bank_holiday(ifeu_equity):
    assert_is_holiday(ifeu_equity, "2026-05-25")


def test_ifeu_equity_summer_bank_holiday(ifeu_equity):
    assert_is_holiday(ifeu_equity, "2026-08-31")


def test_ifeu_equity_boxing_day(ifeu_equity):
    assert_is_holiday(ifeu_equity, "2026-12-28")


def test_ifeu_equity_open_on_1_may(ifeu_equity):
    # Equity does NOT close on continental Labour Day (1 May)
    assert_is_trading_day(ifeu_equity, "2026-05-01")


def test_ifeu_equity_early_close_christmas_eve(ifeu_equity):
    # 24 Dec 2026 winter: 12:50 London = 12:50 UTC
    assert_early_close_utc(ifeu_equity, "2026-12-24", "2026-12-24 12:50:00+00:00")


def test_ifeu_equity_early_close_new_years_eve(ifeu_equity):
    assert_early_close_utc(ifeu_equity, "2026-12-31", "2026-12-31 12:50:00+00:00")


# ---------------------------------------------------------------------------
# 8. ICE Endex Gas/Power
#    Normal close: 23:00 CET = 22:00 UTC (winter) / 21:00 UTC (summer)
#    Early close C (US holidays): 19:30 CET = 18:30 UTC (winter)
#    Early close B (Thanksgiving Friday): 21:00 CET = 20:00 UTC (winter)
#    No early close on Christmas Eve / NYE (status A = early settlement only)
# ---------------------------------------------------------------------------

@pytest.fixture
def endex():
    return ICEEndexGasPowerExchangeCalendar()


def test_endex_instantiates(endex):
    assert endex is not None


def test_endex_regular_trading_days(endex):
    assert_is_trading_day(endex, "2026-03-10")
    assert_is_trading_day(endex, "2026-09-15")


def test_endex_new_years_day(endex):
    assert_is_holiday(endex, "2026-01-01")


def test_endex_good_friday(endex):
    assert_is_holiday(endex, "2026-04-03")


def test_endex_easter_monday(endex):
    assert_is_holiday(endex, "2026-04-06")


def test_endex_christmas_day(endex):
    assert_is_holiday(endex, "2026-12-25")


def test_endex_open_christmas_eve(endex):
    # Status A = normal hours, no early close
    assert_is_trading_day(endex, "2026-12-24")


def test_endex_open_new_years_eve(endex):
    # Status A = normal hours, no early close
    assert_is_trading_day(endex, "2026-12-31")


def test_endex_open_boxing_day(endex):
    # Endex does not observe Boxing Day
    assert_is_trading_day(endex, "2026-12-28")


def test_endex_early_close_thanksgiving(endex):
    # Thanksgiving 2026 = 26 Nov (Thu), status C → 19:30 CET winter = 18:30 UTC
    assert_early_close_utc(endex, "2026-11-26", "2026-11-26 18:30:00+00:00")


def test_endex_early_close_thanksgiving_friday(endex):
    # Thanksgiving Friday 2026 = 27 Nov, status B → 21:00 CET winter = 20:00 UTC
    assert_early_close_utc(endex, "2026-11-27", "2026-11-27 20:00:00+00:00")


def test_endex_early_close_independence_day(endex):
    # 4 Jul 2026 = Saturday → observed Mon 6 Jul (summer, CEST = UTC+2)
    # 19:30 CEST = 17:30 UTC
    assert_early_close_utc(endex, "2026-07-06", "2026-07-06 17:30:00+00:00")


def test_endex_early_close_labor_day(endex):
    # Labor Day 2026 = 7 Sep (Mon, summer, CEST = UTC+2)
    # 19:30 CEST = 17:30 UTC
    assert_early_close_utc(endex, "2026-09-07", "2026-09-07 17:30:00+00:00")


def test_endex_early_close_memorial_day(endex):
    # Memorial Day / Spring BH 2026 = 25 May (Mon, summer, CEST = UTC+2)
    # 19:30 CEST = 17:30 UTC
    assert_early_close_utc(endex, "2026-05-25", "2026-05-25 17:30:00+00:00")


# ---------------------------------------------------------------------------
# 9. ICE Endex Emissions (EUA / GO)
#    Normal close: 18:00 CET = 17:00 UTC (winter) / 16:00 UTC (summer)
#    No early closes at all
# ---------------------------------------------------------------------------

@pytest.fixture
def endex_emissions():
    return ICEEndexEmissionsExchangeCalendar()


def test_endex_emissions_instantiates(endex_emissions):
    assert endex_emissions is not None


def test_endex_emissions_regular_trading_days(endex_emissions):
    assert_is_trading_day(endex_emissions, "2026-03-10")
    assert_is_trading_day(endex_emissions, "2026-09-15")


def test_endex_emissions_new_years_day(endex_emissions):
    assert_is_holiday(endex_emissions, "2026-01-01")


def test_endex_emissions_good_friday(endex_emissions):
    assert_is_holiday(endex_emissions, "2026-04-03")


def test_endex_emissions_easter_monday(endex_emissions):
    assert_is_holiday(endex_emissions, "2026-04-06")


def test_endex_emissions_christmas_day(endex_emissions):
    assert_is_holiday(endex_emissions, "2026-12-25")


def test_endex_emissions_open_boxing_day(endex_emissions):
    assert_is_trading_day(endex_emissions, "2026-12-28")


def test_endex_emissions_open_christmas_eve(endex_emissions):
    # Status A — normal trading hours, no early close
    assert_is_trading_day(endex_emissions, "2026-12-24")


def test_endex_emissions_open_new_years_eve(endex_emissions):
    assert_is_trading_day(endex_emissions, "2026-12-31")


def test_endex_emissions_open_thanksgiving(endex_emissions):
    # US holidays do not affect emissions
    assert_is_trading_day(endex_emissions, "2026-11-26")


def test_endex_emissions_open_may_day_bh(endex_emissions):
    # UK May Day BH does not affect Endex Emissions
    assert_is_trading_day(endex_emissions, "2026-05-04")
