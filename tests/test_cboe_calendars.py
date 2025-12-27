import pandas as pd

from pandas_market_calendars.calendars.cboe import (
    CFEExchangeCalendar,
    CBOEEquityOptionsExchangeCalendar,
    CBOEIndexOptionsExchangeCalendar,
)

calendars = (CFEExchangeCalendar, CBOEEquityOptionsExchangeCalendar, CBOEIndexOptionsExchangeCalendar)


def test_open_time_tz():
    for calendar in calendars:
        cal = calendar()
        assert cal.open_time.tzinfo == cal.tz


def test_close_time_tz():
    for calendar in calendars:
        cal = calendar()
        assert cal.close_time.tzinfo == cal.tz


def test_2016_holidays():
    # new years: jan 1
    # mlk: jan 18
    # presidents: feb 15
    # good friday: mar 25
    # mem day: may 30
    # independence day: july 4
    # labor day: sep 5
    # thanksgiving day: nov 24
    # christmas (observed): dec 26
    # new years (observed): jan 2 2017
    for calendar in calendars:
        cal = calendar()
        good_dates = cal.valid_days("2016-01-01", "2016-12-31")
        for day in [
            "2016-01-01",
            "2016-01-18",
            "2016-02-15",
            "2016-05-30",
            "2016-07-04",
            "2016-09-05",
            "2016-11-24",
            "2016-12-26",
            "2017-01-02",
        ]:
            assert pd.Timestamp(day, tz="UTC") not in good_dates


def test_good_friday_rule():
    # Good friday is a holiday unless Christmas Day or New Years Day is on a Friday
    for calendar in calendars:
        cal = calendar()
        valid_days = cal.valid_days("2015-04-01", "2016-04-01")
        for day in ["2015-04-03", "2016-03-25"]:
            assert day in valid_days


def test_2016_early_closes():
    # early close is day after thanksgiving: nov 25
    for calendar in calendars:
        cal = calendar()
        schedule = cal.schedule("2016-01-01", "2016-12-31")

        dt = pd.Timestamp("2016-11-25")
        assert dt in cal.early_closes(schedule).index

        market_close = schedule.loc[dt].market_close
        market_close = market_close.tz_convert(cal.tz)
        if calendar == CBOEEquityOptionsExchangeCalendar:
            assert market_close.hour == 12
            assert market_close.minute == 0
        else:
            assert market_close.hour == 12
            assert market_close.minute == 15


def test_adhoc_holidays():
    # hurricane sandy: oct 29 2012, oct 30 2012
    # national days of mourning:
    # - apr 27 1994
    # - june 11 2004
    # - jan 2 2007
    for calendar in calendars:
        cal = calendar()
        valid_days = cal.valid_days("1994-01-01", "2012-12-31")
        for day in [
            "1994-04-27",
            "2004-06-11",
            "2007-01-02",
            "2012-10-29",
            "2012-10-30",
        ]:
            print(day)
            assert day not in valid_days


def test_independence_day_early_closes():
    # Test early closes before Independence Day
    # When July 4th is Tue/Wed/Thu/Fri, the previous day should be an early close

    # 2017: July 4th was Tuesday, so July 3rd (Monday) should be early close
    # 2018: July 4th was Wednesday, so July 3rd (Tuesday) should be early close
    # 2019: July 4th was Thursday, so July 3rd (Wednesday) should be early close
    # 2020: July 4th was Saturday, so July 3rd (Friday) should NOT be early close (no rule for this)
    # 2014: July 4th was Friday, so July 3rd (Thursday) should be early close

    test_cases = [
        ("2017-07-03", True),  # July 4th is Tuesday
        ("2018-07-03", True),  # July 4th is Wednesday
        ("2019-07-03", True),  # July 4th is Thursday
        ("2014-07-03", True),  # July 4th is Friday
        ("2015-07-03", False),  # July 4th is Saturday - no early close on Friday
        ("2021-07-02", False),  # July 4th is Sunday (observed Monday July 5) - no early close
    ]

    for date_str, should_be_early_close in test_cases:
        dt = pd.Timestamp(date_str)
        year = dt.year

        for calendar in calendars:
            cal = calendar()
            schedule = cal.schedule(f"{year}-07-01", f"{year}-07-05")

            # Check if the date is in the schedule (i.e., it's a trading day)
            if dt not in schedule.index:
                continue

            if should_be_early_close:
                # Verify it's an early close
                assert dt in cal.early_closes(schedule).index, f"{date_str} should be an early close for {cal.name}"

                market_close = schedule.loc[dt].market_close
                market_close = market_close.tz_convert(cal.tz)

                # CBOE_Equity_Options closes at 12:00, others at 12:15
                if calendar == CBOEEquityOptionsExchangeCalendar:
                    assert (
                        market_close.hour == 12 and market_close.minute == 0
                    ), f"{date_str} should close at 12:00 for {cal.name}, got {market_close.time()}"
                else:
                    assert (
                        market_close.hour == 12 and market_close.minute == 15
                    ), f"{date_str} should close at 12:15 for {cal.name}, got {market_close.time()}"
            else:
                # Verify it's NOT an early close
                assert (
                    dt not in cal.early_closes(schedule).index
                ), f"{date_str} should NOT be an early close for {cal.name}"


if __name__ == "__main__":
    for ref, obj in locals().copy().items():
        if ref.startswith("test_"):
            print("running ", ref)
            obj()
