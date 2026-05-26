import pytest

import pandas as pd
from pandas.testing import assert_index_equal
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.bursa_malaysia import (
    BursaMalaysiaFCPOCalendar,
    BursaMalaysiaFKLICalendar,
)


def test_time_zone():
    assert BursaMalaysiaFCPOCalendar().tz == ZoneInfo("Asia/Kuala_Lumpur")
    assert BursaMalaysiaFKLICalendar().tz == ZoneInfo("Asia/Kuala_Lumpur")


def test_june_hols():
    cal = BursaMalaysiaFCPOCalendar()
    sched_2026 = cal.schedule("2026-05-20", "2026-06-10")
    assert pd.Timestamp("2026-06-01") not in sched_2026.index.get_level_values(0)


def assert_is_holiday(cal, date):
    """Date must NOT appear in the schedule (full closure)."""
    sched = cal.schedule(date, date)
    assert sched.empty, f"{cal.name}: expected {date} to be a holiday"


def assert_is_trading_day(cal, date):
    """Date must appear as a row in the schedule."""
    sched = cal.schedule(date, date)
    assert not sched.empty, f"{cal.name}: expected {date} to be a trading day"


@pytest.fixture
def bursa():
    return BursaMalaysiaFCPOCalendar()


def test_bursa_instantiates(bursa):
    assert bursa is not None


def test_bursa_regular_trading_days(bursa):
    # Ordinary weekdays with no holidays nearby
    assert_is_trading_day(bursa, "2026-03-10")  # Tuesday
    assert_is_trading_day(bursa, "2026-07-14")  # Tuesday


def test_bursa_new_years_day(bursa):
    assert_is_holiday(bursa, "2026-01-01")


def test_bursa_chinese_new_year(bursa):
    # 2026: CNY Day 1 = 17 Feb, Day 2 = 18 Feb
    assert_is_holiday(bursa, "2026-02-17")
    assert_is_holiday(bursa, "2026-02-18")


def test_bursa_thaipusam(bursa):
    # 2026: 1 Feb is Sunday → observed Monday 2 Feb
    assert_is_holiday(bursa, "2026-02-02")


def test_bursa_hari_raya_puasa(bursa):
    # 2026: 21 Mar (Sat) ignored, day 2 (22th) → Mon 23 Mar
    assert_is_trading_day(bursa, "2026-03-20")
    assert_is_holiday(bursa, "2026-03-23")
    assert_is_trading_day(bursa, "2026-03-24")


def test_bursa_labour_day(bursa):
    assert_is_holiday(bursa, "2026-05-01")


def test_bursa_wesak_day(bursa):
    # 2026: 31 May is Sunday → Monday 1 Jun
    assert_is_holiday(bursa, "2026-06-01")


def test_bursa_agong_birthday(bursa):
    # First Monday of June 2026 = 1 Jun (also Wesak sub — both apply)
    # Use 2025: first Monday of June = 2 Jun
    assert_is_holiday(bursa, "2025-06-02")


def test_bursa_hari_raya_haji(bursa):
    # 2026: 27 May (Wed)
    assert_is_holiday(bursa, "2026-05-27")


def test_bursa_awal_muharram(bursa):
    # 2026: 17 Jun
    assert_is_holiday(bursa, "2026-06-17")


def test_bursa_maulidur_rasul(bursa):
    # 2026: 25 Aug
    assert_is_holiday(bursa, "2026-08-25")


def test_bursa_national_day(bursa):
    assert_is_holiday(bursa, "2026-08-31")


def test_bursa_malaysia_day(bursa):
    assert_is_holiday(bursa, "2026-09-16")


def test_bursa_deepavali(bursa):
    # 2026: 8 Nov is Sunday → observed Mon 9 Nov
    assert_is_holiday(bursa, "2026-11-09")


def test_bursa_christmas(bursa):
    assert_is_holiday(bursa, "2026-12-25")


def test_bursa_weekend_not_trading(bursa):
    assert_is_holiday(bursa, "2026-03-07")  # Saturday
    assert_is_holiday(bursa, "2026-03-08")  # Sunday
