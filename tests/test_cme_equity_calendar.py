import pandas as pd
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.cme import CMEEquityExchangeCalendar, CMETradeDateCalendar


def test_time_zone():
    assert CMEEquityExchangeCalendar().tz == ZoneInfo("America/Chicago")
    assert CMEEquityExchangeCalendar().name == "CME_Equity"


def test_sunday_opens():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2020-01-01", "2020-01-31", tz="America/New_York")
    assert pd.Timestamp("2020-01-12 18:00:00", tz="America/New_York") == schedule.loc["2020-01-13", "market_open"]


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


def test_historical_trade_date_open_before_2012_hours_change():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2005-09-12", "2012-11-19", tz="America/Chicago")

    assert schedule.loc["2005-09-12"].market_open == pd.Timestamp("2005-09-11 15:30:00", tz=cme.tz)
    assert schedule.loc["2012-11-16"].market_open == pd.Timestamp("2012-11-15 15:30:00", tz=cme.tz)
    assert schedule.loc["2012-11-19"].market_open == pd.Timestamp("2012-11-18 17:00:00", tz=cme.tz)

    assert schedule.loc["2012-11-16"].market_close == pd.Timestamp("2012-11-16 15:15:00", tz=cme.tz)
    assert schedule.loc["2012-11-16"].break_start == schedule.loc["2012-11-16"].break_end
    assert cme.open_at_time(schedule, "2012-11-16 15:14:59-06:00") is True
    assert cme.open_at_time(schedule, "2012-11-16 15:15:00-06:00") is False
    assert cme.open_at_time(schedule, "2012-11-16 15:20:00-06:00") is False
    assert cme.open_at_time(schedule, "2012-11-19 15:31:00-06:00") is True


def test_historical_trade_date_time_helpers_match_schedule_cutovers():
    cme = CMEEquityExchangeCalendar()

    assert cme.open_time_on("2005-09-12").hour == 15
    assert cme.open_time_on("2005-09-12").minute == 30
    assert cme.close_time_on("2005-09-12").hour == 15
    assert cme.close_time_on("2005-09-12").minute == 15
    assert cme.break_end_on("2005-09-12").hour == 15
    assert cme.break_end_on("2005-09-12").minute == 15

    assert cme.open_time_on("2012-11-19").hour == 17
    assert cme.close_time_on("2012-11-19").hour == 16
    assert cme.break_end_on("2012-11-19").hour == 15
    assert cme.break_end_on("2012-11-19").minute == 30


def test_2023_good_friday_has_early_close_session():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2023-04-06", "2023-04-10", tz="America/New_York")

    session = schedule.loc["2023-04-07"]
    assert session.market_open == pd.Timestamp("2023-04-06 18:00:00", tz="America/New_York")
    assert session.market_close == pd.Timestamp("2023-04-07 09:15:00", tz="America/New_York")


def test_trade_date_calendar_excludes_equity_early_close_holidays():
    trade_dates = CMETradeDateCalendar().valid_days("2024-05-24", "2024-05-29")
    equity_schedule = CMEEquityExchangeCalendar().schedule("2024-05-24", "2024-05-29", tz="America/Chicago")

    assert pd.Timestamp("2024-05-27", tz="UTC") not in trade_dates
    assert equity_schedule.loc["2024-05-27"].market_close == pd.Timestamp("2024-05-27 12:00:00", tz="America/Chicago")


def test_trade_date_calendar_excludes_settlement_holidays_without_dropping_equity_sessions():
    cme = CMEEquityExchangeCalendar()
    early_close_dates = [
        "2022-01-17",
        "2022-02-21",
        "2022-05-30",
        "2022-06-20",
        "2022-07-04",
        "2022-09-05",
        "2022-11-24",
        "2023-01-16",
        "2023-02-20",
        "2023-05-29",
        "2023-06-19",
        "2023-07-04",
        "2023-09-04",
        "2023-11-23",
        "2024-01-15",
        "2024-02-19",
    ]

    trade_dates = CMETradeDateCalendar().valid_days("2022-01-01", "2024-02-29")
    schedule = cme.schedule("2022-01-01", "2024-02-29", tz=cme.tz)

    for date in early_close_dates:
        timestamp = pd.Timestamp(date, tz="UTC")
        expected_close = pd.Timestamp(f"{date} 12:00:00", tz=cme.tz)
        assert timestamp not in trade_dates
        assert schedule.loc[date].market_close == expected_close


def test_good_friday_2026_has_early_close_session():
    cme = CMEEquityExchangeCalendar()
    schedule = cme.schedule("2026-04-01", "2026-04-07", tz="America/New_York")

    session = schedule.loc["2026-04-03"]
    assert session.market_open == pd.Timestamp("2026-04-02 18:00:00", tz="America/New_York")
    assert session.market_close == pd.Timestamp("2026-04-03 09:15:00", tz="America/New_York")
