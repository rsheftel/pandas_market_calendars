"""Tests for MEFFIBEXFuturesCalendar"""

import pandas as pd
from pandas_market_calendars.calendars.meff import MEFFIBEXFuturesCalendar


def _sched(cal, date):
    return cal.schedule(date, date)


def _is_holiday(cal, date):
    return _sched(cal, date).empty


def _close(cal, date):
    return _sched(cal, date)["market_close"].iloc[0]


# ---------------------------------------------------------------------------
# MEFF IBEX 35
# ---------------------------------------------------------------------------


def test_meff_instantiates():
    assert MEFFIBEXFuturesCalendar() is not None


def test_meff_epiphany_closed():
    # Spanish national holiday missing from XMAD base
    assert _is_holiday(MEFFIBEXFuturesCalendar(), "2026-01-06")


def test_meff_good_friday_closed():
    assert _is_holiday(MEFFIBEXFuturesCalendar(), "2026-04-03")


def test_meff_fiesta_nacional_closed():
    assert _is_holiday(MEFFIBEXFuturesCalendar(), "2026-10-12")


def test_meff_immaculate_conception_closed():
    assert _is_holiday(MEFFIBEXFuturesCalendar(), "2026-12-08")


def test_meff_normal_hours():
    # CET winter = UTC+1; 09:00 CET = 08:00 UTC, 17:35 CET = 16:35 UTC
    sched = _sched(MEFFIBEXFuturesCalendar(), "2026-03-10")
    assert sched["market_open"].iloc[0] == pd.Timestamp("2026-03-10 08:00:00+00:00")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 16:35:00+00:00")


def test_meff_christmas_eve_early_close():
    # 14:00 CET winter = 13:00 UTC
    assert _close(MEFFIBEXFuturesCalendar(), "2026-12-24") == pd.Timestamp("2026-12-24 13:00:00+00:00")


def test_meff_new_years_eve_early_close():
    assert _close(MEFFIBEXFuturesCalendar(), "2026-12-31") == pd.Timestamp("2026-12-31 13:00:00+00:00")
