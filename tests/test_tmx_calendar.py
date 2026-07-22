import pandas as pd
from pandas.testing import assert_index_equal
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.tmx import (
    MonExBondExchangeCalendar,
    MonExIndexExchangeCalendar,
    MonExStirExchangeCalendar,
)


def test_time_zone():
    assert MonExBondExchangeCalendar().tz == ZoneInfo("Canada/Eastern")
    assert MonExIndexExchangeCalendar().tz == ZoneInfo("Canada/Eastern")
    assert MonExStirExchangeCalendar().tz == ZoneInfo("Canada/Eastern")


def test_rememberance_day_closed_bonds():
    cal = MonExBondExchangeCalendar()
    sched_2018 = cal.schedule("2018-10-25", "2018-11-25")
    assert sched_2018.loc[pd.Timestamp("2018-11-09"), "market_close"] == pd.Timestamp("2018-11-09 18:30 +0")
    assert pd.Timestamp("2018-11-12") not in sched_2018.index.get_level_values(0)


def test_rememberance_day_open_index():
    cal = MonExIndexExchangeCalendar()
    sched_2018 = cal.schedule("2018-10-25", "2018-11-25")
    assert sched_2018.loc[pd.Timestamp("2018-11-09"), "market_close"] == pd.Timestamp("2018-11-09 21:30 +0")
    assert pd.Timestamp("2018-11-12") in sched_2018.index.get_level_values(0)
