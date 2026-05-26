import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars import get_calendar
from pandas_market_calendars.calendars.eurex import EUREXExchangeCalendar, EUREXPrePostExchangeCalendar


def test_time_zone():
    assert EUREXExchangeCalendar().tz == ZoneInfo("Europe/Berlin")
    assert EUREXExchangeCalendar().name == "EUREX"


def test_regular_market_times():
    eurex = EUREXExchangeCalendar()

    assert "pre" not in eurex.regular_market_times
    assert "post" not in eurex.regular_market_times
    assert eurex.market_times == ["market_open", "market_close"]
    assert eurex.regular_market_times["market_open"] == ((None, pd.Timestamp("08:00").time()),)
    assert eurex.regular_market_times["market_close"] == ((None, pd.Timestamp("22:00").time()),)

    schedule = eurex.schedule(
        "2025-03-07",
        "2025-03-07",
        tz="Europe/Berlin",
    )
    session = schedule.loc["2025-03-07"]
    assert session.market_open == pd.Timestamp("2025-03-07 08:00", tz=eurex.tz)
    assert session.market_close == pd.Timestamp("2025-03-07 22:00", tz=eurex.tz)


def test_pre_post_market_times():
    eurex = EUREXPrePostExchangeCalendar()

    assert eurex.tz == ZoneInfo("UTC")
    assert eurex.name == "EUREX_PrePost"
    assert eurex.market_times == ["pre", "market_open", "market_close", "post"]
    assert eurex.regular_market_times["pre"] == ((None, pd.Timestamp("00:15").time()),)
    assert eurex.regular_market_times["market_open"] == ((None, pd.Timestamp("08:00").time()),)
    assert eurex.regular_market_times["market_close"] == ((None, pd.Timestamp("16:30").time()),)
    assert eurex.regular_market_times["post"] == ((None, pd.Timestamp("21:00").time()),)

    assert get_calendar("EUREX_PrePost").name == "EUREX_PrePost"
    assert get_calendar("EUREX_Extended").name == "EUREX_PrePost"

    schedule = eurex.schedule(
        "2025-03-07",
        "2025-03-07",
        start="pre",
        end="post",
    )
    session = schedule.loc["2025-03-07"]
    assert session.pre == pd.Timestamp("2025-03-07 00:15", tz="UTC")
    assert session.market_open == pd.Timestamp("2025-03-07 08:00", tz="UTC")
    assert session.market_close == pd.Timestamp("2025-03-07 16:30", tz="UTC")
    assert session.post == pd.Timestamp("2025-03-07 21:00", tz="UTC")

    early_close = eurex.schedule(
        "2025-12-24",
        "2025-12-24",
        start="pre",
        end="post",
    ).loc["2025-12-24"]
    assert early_close.market_close == pd.Timestamp("2025-12-24 11:30", tz="UTC")
    assert early_close.post == pd.Timestamp("2025-12-24 11:30", tz="UTC")

    post_only = eurex.schedule(
        "2025-12-24",
        "2025-12-24",
        market_times=["post"],
    ).loc["2025-12-24"]
    assert post_only.post == pd.Timestamp("2025-12-24 11:30", tz="UTC")

    special_post = eurex.special_dates("post", "2025-12-24", "2025-12-24")
    assert special_post.loc[pd.Timestamp("2025-12-24")] == pd.Timestamp("2025-12-24 11:30", tz="UTC")


def test_2016_holidays():
    # good friday: 2016-03-25
    # May 1st: on a weekend, not rolled forward
    # christmas: on a weekend, not rolled forward
    # boxing day: 2016-12-26
    # new years (observed): 2016-01-01
    eurex = EUREXExchangeCalendar()
    good_dates = eurex.valid_days("2016-01-01", "2016-12-31")
    for date in ["2016-03-25", "2016-01-01", "2016-12-26"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates
    for date in ["2016-05-02"]:
        assert pd.Timestamp(date, tz="UTC") in good_dates


def test_2017_holidays():
    # good friday: 2017-04-14
    # May 1st: 2017-05-01
    # christmas (observed): 2017-12-25
    # new years (observed): on a weekend, not rolled forward
    eurex = EUREXExchangeCalendar()
    good_dates = eurex.valid_days("2017-01-01", "2017-12-31")
    for date in ["2016-04-14", "2017-05-01", "2017-12-25"]:
        assert pd.Timestamp(date, tz="UTC") not in good_dates
    for date in ["2017-01-02"]:
        assert pd.Timestamp(date, tz="UTC") in good_dates
