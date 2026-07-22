import pandas as pd

from pandas_market_calendars.calendars.ice import (
    ICEExchangeCalendar,
    ICEUSCanolaCalendar,
    ICEUSDailyGoldSilverCalendar,
    ICEUSFinancialsCalendar,
    ICEUSCoffeeCalendar,
    ICEUSCocoaCalendar,
    ICEUSCottonCalendar,
    ICEUSSugar11Calendar,
    ICEUSSugar16Calendar,
    ICEUSFxCalendar,
    ICEUSEnergiesCalendar
)


def test_test_name():
    assert ICEExchangeCalendar().name == "ICE"


def test_hurricane_sandy_one_day():
    dates_open = ICEExchangeCalendar().valid_days("2012-10-01", "2012-11-01")

    # closed first day of hurricane sandy
    assert pd.Timestamp("2012-10-29", tz="UTC") not in dates_open

    # ICE wasn't closed on day 2 of hurricane sandy
    assert pd.Timestamp("2012-10-30", tz="UTC") in dates_open


def test_2016_holidays():
    # 2016 holidays:
    # new years: 2016-01-01
    # good friday: 2016-03-25
    # christmas (observed): 2016-12-26

    ice = ICEExchangeCalendar()
    good_dates = ice.valid_days("2016-01-01", "2016-12-31")
    for date in ["2016-01-01", "2016-03-25", "2016-12-26"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_2016_early_closes():
    # 2016 early closes
    # mlk: 2016-01-18
    # presidents: 2016-02-15
    # mem day: 2016-05-30
    # independence day: 2016-07-04
    # labor: 2016-09-05
    # thanksgiving: 2016-11-24

    ice = ICEExchangeCalendar()
    schedule = ice.schedule("2016-01-01", "2016-12-31")
    early_closes = ice.early_closes(schedule)
    for date in [
        "2016-01-18",
        "2016-02-15",
        "2016-05-30",
        "2016-07-04",
        "2016-09-05",
        "2016-11-24",
    ]:
        dt = pd.Timestamp(date)
        assert dt in early_closes.index

        market_close = schedule.loc[dt].market_close
        # all ICE early closes are 1 pm local
        assert market_close.tz_convert(ice.tz).hour == 13


def _sched(cal, date):
    return cal.schedule(date, date)


def _is_holiday(cal, date):
    return _sched(cal, date).empty


def _is_trading(cal, date):
    return not _sched(cal, date).empty


# ---------------------------------------------------------------------------
# Softs (Cocoa, Coffee, Cotton, FCOJ, Sugar 11, Sugar 16)
# ---------------------------------------------------------------------------


def test_softs_instantiates():
    for cal in [
        ICEUSCoffeeCalendar,
        ICEUSCocoaCalendar,
        ICEUSCottonCalendar,
        ICEUSSugar11Calendar,
        ICEUSSugar16Calendar
    ]:
        assert cal() is not None


def test_softs_new_years_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-01-01")


def test_softs_mlk_closed():
    for cal in [
        ICEUSCoffeeCalendar,
        ICEUSCocoaCalendar,
        ICEUSCottonCalendar,
        ICEUSSugar11Calendar,
        ICEUSSugar16Calendar
    ]:
        assert _is_holiday(cal(), "2026-01-19")


def test_softs_presidents_day_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-02-16")


def test_softs_good_friday_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-04-03")


def test_softs_memorial_day_closed():
    assert _is_holiday(ICEUSCocoaCalendar(), "2026-05-25")


def test_softs_juneteenth_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-06-19")


def test_softs_independence_day_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-07-03")


def test_softs_labor_day_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-09-07")


def test_softs_thanksgiving_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-11-26")


def test_softs_christmas_closed():
    assert _is_holiday(ICEUSCoffeeCalendar(), "2026-12-25")


def test_softs_columbus_day_open():
    # Columbus Day is NOT a softs closure
    assert _is_trading(ICEUSCoffeeCalendar(), "2026-10-12")


def test_softs_veterans_day_open():
    assert _is_trading(ICEUSCoffeeCalendar(), "2026-11-11")


def test_softs_normal_open():
    sched = _sched(ICEUSSugar11Calendar(), "2026-03-10")
    # Sugar 11 opens at 03:30 ET; EDT (UTC-4) in March -> 07:30 UTC
    assert sched["market_open"].iloc[0] == pd.Timestamp("2026-03-10 07:30:00+00:00")


# ---------------------------------------------------------------------------
# FX (DX)
# ---------------------------------------------------------------------------


def test_dx_instantiates():
    assert ICEUSFxCalendar() is not None


def test_dx_new_years_closed():
    assert _is_holiday(ICEUSFxCalendar(), "2026-01-01")


def test_dx_christmas_closed():
    assert _is_holiday(ICEUSFxCalendar(), "2026-12-25")


def test_dx_good_friday_open():
    # KEY difference from existing ICEExchangeCalendar — DX is open Good Friday
    assert _is_trading(ICEUSFxCalendar(), "2026-04-03")


def test_dx_mlk_open():
    assert _is_trading(ICEUSFxCalendar(), "2026-01-19")


def test_dx_presidents_day_open():
    assert _is_trading(ICEUSFxCalendar(), "2026-02-16")


def test_dx_memorial_day_open():
    assert _is_trading(ICEUSFxCalendar(), "2026-05-25")


def test_dx_labor_day_open():
    assert _is_trading(ICEUSFxCalendar(), "2026-09-07")


def test_dx_thanksgiving_open():
    assert _is_trading(ICEUSFxCalendar(), "2026-11-26")


def test_dx_normal_hours():
    sched = _sched(ICEUSFxCalendar(), "2026-03-10")
    # 20:00 ET prev day (Mar 9 EDT = UTC-4) = 00:00 UTC Mar 10
    assert sched["market_open"].iloc[0] == pd.Timestamp("2026-03-10 00:00:00+00:00")
    # 17:00 ET (EDT = UTC-4) = 21:00 UTC
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 21:00:00+00:00")


# ---------------------------------------------------------------------------
# Canola
# ---------------------------------------------------------------------------


def test_canola_instantiates():
    assert ICEUSCanolaCalendar() is not None


def test_canola_truth_reconciliation_closed():
    assert _is_holiday(ICEUSCanolaCalendar(), "2026-09-30")


def test_canola_remembrance_day_closed():
    assert _is_holiday(ICEUSCanolaCalendar(), "2026-11-11")


def test_canola_canadian_thanksgiving_closed():
    assert _is_holiday(ICEUSCanolaCalendar(), "2026-10-12")


def test_canola_victoria_day_closed():
    assert _is_holiday(ICEUSCanolaCalendar(), "2026-05-18")


def test_canola_mlk_open():
    assert _is_trading(ICEUSCanolaCalendar(), "2026-01-19")


def test_canola_us_thanksgiving_open():
    assert _is_trading(ICEUSCanolaCalendar(), "2026-11-26")


def test_canola_normal_hours():
    sched = _sched(ICEUSCanolaCalendar(), "2026-03-10")
    # 09:00 ET (EDT=UTC-4) = 13:00 UTC; 13:00 ET = 17:00 UTC
    assert sched["market_open"].iloc[0] == pd.Timestamp("2026-03-10 00:00:00+00:00")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 18:20:00+00:00")


# ---------------------------------------------------------------------------
# Energy & Environmental
# ---------------------------------------------------------------------------


def test_energy_instantiates():
    assert ICEUSEnergiesCalendar() is not None


def test_energy_good_friday_closed():
    assert _is_holiday(ICEUSEnergiesCalendar(), "2026-04-03")


def test_energy_new_years_closed():
    assert _is_holiday(ICEUSEnergiesCalendar(), "2026-01-01")


def test_energy_christmas_closed():
    assert _is_holiday(ICEUSEnergiesCalendar(), "2026-12-25")


def test_energy_memorial_day_open():
    # Key difference from softs — energy stays open
    assert _is_trading(ICEUSEnergiesCalendar(), "2026-05-25")


def test_energy_boxing_day_open():
    assert _is_trading(ICEUSEnergiesCalendar(), "2026-12-28")


def test_energy_normal_hours():
    sched = _sched(ICEUSEnergiesCalendar(), "2026-03-10")
    assert sched["market_open"].iloc[0] == pd.Timestamp("2026-03-09 23:50:00+00:00")
    assert sched["market_close"].iloc[0] == pd.Timestamp("2026-03-10 22:00:00+00:00")


# ---------------------------------------------------------------------------
# Daily Gold & Silver
# ---------------------------------------------------------------------------


def test_gold_instantiates():
    assert ICEUSDailyGoldSilverCalendar() is not None


def test_gold_good_friday_closed():
    assert _is_holiday(ICEUSDailyGoldSilverCalendar(), "2026-04-03")


def test_gold_memorial_day_closed():
    # Different from energy — gold closes for Memorial Day
    assert _is_holiday(ICEUSDailyGoldSilverCalendar(), "2026-05-25")


def test_gold_boxing_day_closed():
    # Different from energy — gold closes for Boxing Day
    assert _is_holiday(ICEUSDailyGoldSilverCalendar(), "2026-12-28")


def test_gold_labor_day_open():
    assert _is_trading(ICEUSDailyGoldSilverCalendar(), "2026-09-07")


def test_gold_thanksgiving_open():
    assert _is_trading(ICEUSDailyGoldSilverCalendar(), "2026-11-26")
