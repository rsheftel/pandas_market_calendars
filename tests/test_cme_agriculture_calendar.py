import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.cme import CMEAgricultureExchangeCalendar
from pandas_market_calendars.calendars.cme_globex_agriculture import (
    CMEGlobexLivestockExchangeCalendar,
    CMEGlobexGrainsAndOilseedsExchangeCalendar
)


def test_time_zone():
    assert CMEAgricultureExchangeCalendar().tz == ZoneInfo("America/Chicago")
    assert CMEAgricultureExchangeCalendar().name == "CME_Agriculture"


def test_regular_market_times_match_grains_public_hours():
    cme = CMEAgricultureExchangeCalendar()
    schedule = cme.schedule("2024-11-25", "2024-11-25", tz="America/Chicago")
    session = schedule.loc["2024-11-25"]
    assert session.market_open == pd.Timestamp("2024-11-24 19:00:00", tz=cme.tz)
    assert session.break_start == pd.Timestamp("2024-11-25 07:45:00", tz=cme.tz)
    assert session.break_end == pd.Timestamp("2024-11-25 08:30:00", tz=cme.tz)
    assert session.market_close == pd.Timestamp("2024-11-25 13:20:00", tz=cme.tz)


def test_2020_holidays():
    # martin luthur king: 2020-01-20
    # president's day: 2020-02-17
    # good friday: 2020-04-10
    # memorial day: 2020-05-25
    # independence day: 2020-04-02 and 2020-04-03
    # labor day: 2020-09-07
    # thanksgiving: 2020-11-25, 2020-11-26
    # christmas (observed): 2020-12-25, 2020-12-27
    # new years (observed): 2021-01-01
    #
    # These dates should be excluded, but are still in the calendar:
    # - 2020-04-02
    # - 2020-04-03
    # - 2020-11-25
    cme = CMEAgricultureExchangeCalendar()
    good_dates = cme.valid_days("2020-01-01", "2021-01-10")
    for date in [
        "2020-01-20",
        "2020-02-17",
        "2020-04-10",
        "2020-05-25",
        "2020-09-07",
        "2020-11-26",
        "2020-12-25",
        "2020-12-27",
        "2021-01-01",
    ]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_dec_jan():
    cme = CMEAgricultureExchangeCalendar()
    schedule = cme.schedule("2020-12-30", "2021-01-10")

    assert schedule["market_open"].iloc[0] == pd.Timestamp("2020-12-30 01:00:00", tz="UTC")
    assert schedule["market_close"].iloc[6] == pd.Timestamp("2021-01-08 19:20:00", tz="UTC")


def test_livestock_2014_to_2016_hours():
    cme = CMEGlobexLivestockExchangeCalendar()
    # Monday
    schedule = cme.schedule("2014-09-29", "2014-10-03")
    assert schedule["market_open"].iloc[0] == pd.Timestamp("2014-09-29 14:05:00", tz="UTC")
    assert schedule["market_close"].iloc[0] == pd.Timestamp("2014-09-29 21:00:00", tz="UTC")
    # Tuesday
    assert schedule["market_open"].iloc[1] == pd.Timestamp("2014-09-29 22:00:00", tz="UTC")
    assert schedule["market_close"].iloc[1] == pd.Timestamp("2014-09-30 21:00:00", tz="UTC")
    # Friday
    assert schedule["market_open"].iloc[4] == pd.Timestamp("2014-10-02 22:00:00", tz="UTC")
    assert schedule["market_close"].iloc[4] == pd.Timestamp("2014-10-03 18:55:00", tz="UTC")


def test_livestock_pre_2014_hours():
    cme = CMEGlobexLivestockExchangeCalendar()
    # Monday
    schedule = cme.schedule("2015-09-28", "2015-10-02")
    assert schedule["market_open"].iloc[0] == pd.Timestamp("2015-09-28 14:05:00", tz="UTC")
    assert schedule["market_close"].iloc[0] == pd.Timestamp("2015-09-28 21:00:00", tz="UTC")
    # Tuesday
    assert schedule["market_open"].iloc[1] == pd.Timestamp("2015-09-29 13:00:00", tz="UTC")
    assert schedule["market_close"].iloc[1] == pd.Timestamp("2015-09-29 21:00:00", tz="UTC")
    # Friday
    assert schedule["market_open"].iloc[4] == pd.Timestamp("2015-10-02 13:00:00", tz="UTC")
    assert schedule["market_close"].iloc[4] == pd.Timestamp("2015-10-02 18:55:00", tz="UTC")

def test_aggs_pre_2012_hours():
    cme = CMEGlobexGrainsAndOilseedsExchangeCalendar()
    schedule = cme.schedule("2011-09-30", "2011-09-30")
    assert schedule["market_open"].iloc[0] == pd.Timestamp("2011-09-29 23:00:00", tz="UTC")
    assert schedule["break_start"].iloc[0] == pd.Timestamp("2011-09-30 12:15:00", tz="UTC")
    assert schedule["break_end"].iloc[0] == pd.Timestamp("2011-09-30 14:30:00", tz="UTC")
    assert schedule["market_close"].iloc[0] == pd.Timestamp("2011-09-30 18:15:00", tz="UTC")
    

def test_aggs_2012_2013_hours():
    cme = CMEGlobexGrainsAndOilseedsExchangeCalendar()
    schedule = cme.schedule("2012-09-28", "2012-09-28")
    assert schedule["market_open"].iloc[0] == pd.Timestamp("2012-09-27 22:00:00", tz="UTC")
    assert schedule["break_start"].iloc[0] == pd.Timestamp("2012-09-27 22:00:00", tz="UTC")
    assert schedule["break_end"].iloc[0] == pd.Timestamp("2012-09-27 22:00:00", tz="UTC")
    assert schedule["market_close"].iloc[0] == pd.Timestamp("2012-09-28 19:00:00", tz="UTC")
