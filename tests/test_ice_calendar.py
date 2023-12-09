import pandas as pd

from pandas_market_calendars.calendars.ice import ICEExchangeCalendar


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
