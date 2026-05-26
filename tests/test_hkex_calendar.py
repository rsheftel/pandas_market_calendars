import datetime

import pandas as pd
from zoneinfo import ZoneInfo


from pandas_market_calendars.calendars.hkex import (
    HKEXExchangeCalendar,
    HKFEDomesticExchangeCalendar,
    HKFEA50ExchangeCalendar,
    HKFECNHExchangeCalendar,
    HKFETaiwanExchangeCalendar
)


def _is_holiday(cal, date):
    return cal.schedule(date, date).empty


def _is_trading(cal, date):
    return not cal.schedule(date, date).empty


def test_time_zone():
    assert HKEXExchangeCalendar().tz == ZoneInfo("Asia/Shanghai")
    assert HKEXExchangeCalendar().name == "HKEX"


def test_2018_holidays():
    hkex = HKEXExchangeCalendar()
    trading_days = hkex.valid_days("2018-01-01", "2018-12-31")
    holidays = [
        "2018-01-01",
        "2018-02-16",
        "2018-02-17",
        "2018-02-18",
        "2018-02-19",
        "2018-03-30",
        "2018-04-02",
        "2018-04-05",
        "2018-05-01",
        "2018-05-22",
        "2018-06-18",
        "2018-07-02",
        "2018-09-25",
        "2018-10-01",
        "2018-10-17",
        "2018-12-25",
        "2018-12-26",
    ]
    for date in holidays:
        assert pd.Timestamp(date, tz="UTC") not in trading_days
    for date in ["2018-05-02"]:
        assert pd.Timestamp(date, tz="UTC") in trading_days


def test_hkex_closes_at_lunch():
    hkex = HKEXExchangeCalendar()
    schedule = hkex.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=ZoneInfo("Asia/Shanghai")),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert hkex.open_at_time(
        schedule=schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=ZoneInfo("Asia/Shanghai")),
    )

    assert not hkex.open_at_time(
        schedule=schedule,
        timestamp=datetime.datetime(2015, 1, 14, 12, 10, tzinfo=ZoneInfo("Asia/Shanghai")),
    )


# ---------------------------------------------------------------------------
# HKFE Non-Holiday (HSI, MHI, HHI, MCH, HTI)
# ---------------------------------------------------------------------------


def test_hkfe_non_holiday_instantiates():
    assert HKFEDomesticExchangeCalendar() is not None


def test_hkfe_non_holiday_closes_on_hk_holiday():
    cal = HKFEDomesticExchangeCalendar()
    # Labour Day 2026 — standard HK public holiday
    assert _is_holiday(cal, "2026-05-01")


def test_hkfe_non_holiday_closes_on_lunar_new_year():
    cal = HKFEDomesticExchangeCalendar()
    # LNY Day 1 2026 — 17 Feb
    assert _is_holiday(cal, "2026-02-17")


def test_hkfe_non_holiday_early_close_lny_eve():
    cal = HKFEDomesticExchangeCalendar()
    # LNY Eve 2026 — 16 Feb, morning session only (close 12:00 HKT = 04:00 UTC)
    sched = cal.schedule("2026-02-16", "2026-02-16")
    assert not sched.empty
    close = sched["market_close"].iloc[0]
    assert close == pd.Timestamp("2026-02-16 04:00:00+00:00")


def test_hkfe_non_holiday_t1_session_modelled():
    cal = HKFEDomesticExchangeCalendar()
    # Normal day: break_start=16:30 HKT=08:30 UTC, break_end=17:15 HKT=09:15 UTC
    sched = cal.schedule("2026-03-10", "2026-03-10")
    assert "break_start" in sched.columns
    assert "break_end" in sched.columns
    break_start = sched["break_start"].iloc[0]
    break_end = sched["break_end"].iloc[0]
    assert break_start == pd.Timestamp("2026-03-10 08:30:00+00:00")
    assert break_end == pd.Timestamp("2026-03-10 09:15:00+00:00")


# ---------------------------------------------------------------------------
# HKFE Holiday Trading (MTW, MCA, CUS)
# ---------------------------------------------------------------------------


def test_hkfe_holiday_trading_instantiates():
    assert HKFEA50ExchangeCalendar() is not None
    assert HKFECNHExchangeCalendar() is not None
    assert HKFETaiwanExchangeCalendar() is not None


def test_hkfe_holiday_trading_open_on_hk_holiday():
    cal = HKFEA50ExchangeCalendar()
    # Labour Day 2026 — HK holiday but MSCI/FX contracts trade
    assert _is_trading(cal, "2026-05-01")


def test_hkfe_holiday_trading_closed_new_years_day():
    for cal in [
        HKFEA50ExchangeCalendar(),
        HKFECNHExchangeCalendar(),
        HKFETaiwanExchangeCalendar()
    ]:
        # New Year's Day is the one exception — all contracts closed
        assert _is_holiday(cal, "2026-01-01")


def test_hkfe_holiday_trading_open_on_lunar_new_year():
    cal = HKFEA50ExchangeCalendar()
    # LNY Day 1 2026 — MSCI/FX contracts trade through HK public holidays
    assert _is_trading(cal, "2026-02-17")
