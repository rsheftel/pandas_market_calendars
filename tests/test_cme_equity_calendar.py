import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.cme import CMEEquityExchangeCalendar


def test_time_zone():
    assert CMEEquityExchangeCalendar().tz == ZoneInfo("America/Chicago")
    assert CMEEquityExchangeCalendar().name == "CME_Equity"


def test_sunday_opens():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2020-01-01", "2020-01-31", tz="America/New_York")
    assert (
        pd.Timestamp("2020-01-12 18:00:00", tz="America/New_York")
        == schedule.loc["2020-01-13", "market_open"]
    )


def test_2016_holidays():
    # good friday: 2016-03-25
    # christmas (observed): 2016-12-26
    # new years (observed): 2016-01-02
    cme = CMEEquityExchangeCalendar()
    good_dates = cme.valid_days("2016-01-01", "2016-12-31")
    for date in ["2016-03-25", "2016-12-26", "2016-01-02"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates


def test_2016_early_closes():
    # mlk day: 2016-01-18
    # presidents: 2016-02-15
    # mem day: 2016-05-30
    # july 4: 2016-07-04
    # labor day: 2016-09-05
    # thanksgiving: 2016-11-24

    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2016-01-01", "2016-12-31")
    early_closes = cme.early_closes(schedule).index

    for date in [
        "2016-01-18",
        "2016-02-15",
        "2016-05-30",
        "2016-07-04",
        "2016-09-05",
        "2016-11-24",
    ]:
        dt = pd.Timestamp(date)
        assert dt in early_closes

        market_close = schedule.loc[dt].market_close
        assert market_close.tz_convert(cme.tz).hour == 12


def test_dec_jan():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2016-12-30", "2017-01-10")

    assert schedule["market_open"].iloc[0] == pd.Timestamp("2016-12-29 23:00:00", tz="UTC")
    assert schedule["market_close"].iloc[6] == pd.Timestamp("2017-01-10 22:00:00", tz="UTC")
