import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.cme import CMEAgricultureExchangeCalendar


def test_time_zone():
    assert CMEAgricultureExchangeCalendar().tz == ZoneInfo("America/Chicago")
    assert CMEAgricultureExchangeCalendar().name == "CME_Agriculture"


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

    assert schedule["market_open"].iloc[0] == pd.Timestamp(
        "2020-12-29 23:01:00", tz="UTC"
    )
    assert schedule["market_close"].iloc[6] == pd.Timestamp(
        "2021-01-08 23:00:00", tz="UTC"
    )
