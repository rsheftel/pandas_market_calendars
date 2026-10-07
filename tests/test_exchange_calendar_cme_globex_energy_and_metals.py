import pandas as pd
from pandas.testing import assert_index_equal
from zoneinfo import ZoneInfo

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.cme_globex_energy_and_metals import (
    CMEGlobexEnergyAndMetalsExchangeCalendar,
)


cal = CMEGlobexEnergyAndMetalsExchangeCalendar()


def test_time_zone():
    assert cal.tz == ZoneInfo("America/Chicago")
    assert cal.name == "CMEGlobex_EnergyAndMetals"


def test_open_time_tz():
    assert cal.open_time.tzinfo == cal.tz


def test_close_time_tz():
    assert cal.close_time.tzinfo == cal.tz


def test_weekmask():
    assert cal.weekmask == "Mon Tue Wed Thu Fri"


def _test_holidays(holidays, start, end):
    df = pd.DataFrame(cal.holidays().holidays, columns=["holidays"])
    mask = (df["holidays"] >= start) & (df["holidays"] <= end)
    df = df[mask]
    assert len(holidays) == len(df)
    df = df.set_index(["holidays"])
    df.index = df.index.tz_localize("UTC")
    assert_index_equal(pd.DatetimeIndex(holidays), df.index, check_names=False)
    valid_days = cal.valid_days(start, end)
    for h in holidays:
        assert h not in valid_days


def _test_no_special_opens(start, end):
    assert len(cal.late_opens(cal.schedule(start, end))) == 0


def _test_no_special_closes(start, end):
    assert len(cal.early_closes(cal.schedule(start, end))) == 0


def _test_no_special_opens_closes(start, end):
    _test_no_special_opens(start, end)
    _test_no_special_closes(start, end)


def _test_verify_late_open_time(schedule, timestamp):
    date = pd.Timestamp(pd.Timestamp(timestamp).tz_convert("UTC").date())
    if date in schedule.index:
        return schedule.at[date, "market_open"] == timestamp
    else:
        return False


def _test_has_late_opens(late_opens, start, end):
    schedule = cal.schedule(start, end)
    expected = cal.late_opens(schedule)
    assert len(expected) == len(late_opens)
    for ts in late_opens:
        assert _test_verify_late_open_time(schedule, ts) is True


def _test_verify_early_close_time(schedule, timestamp):
    date = pd.Timestamp(pd.Timestamp(timestamp).tz_convert("UTC").date())
    if date in schedule.index:
        return schedule.at[date, "market_close"] == timestamp
    else:
        return False


def _test_has_early_closes(early_closes, start, end):
    schedule = cal.schedule(start, end)
    expected = cal.early_closes(schedule)
    assert len(expected) == len(early_closes)
    for ts in early_closes:
        assert _test_verify_early_close_time(schedule, ts) is True


# Reported against CME's published 2026 Energy and Metals schedule:
# https://github.com/rsheftel/pandas_market_calendars/issues/464
def test_2026_energy_and_metals_early_closes():
    expected_closes = {
        "2026-06-19": pd.Timestamp("2026-06-19 13:00", tz="America/New_York"),
        "2026-07-03": pd.Timestamp("2026-07-03 13:00", tz="America/New_York"),
        "2026-09-07": pd.Timestamp("2026-09-07 14:30", tz="America/New_York"),
        "2026-11-27": pd.Timestamp("2026-11-27 14:45", tz="America/New_York"),
        "2026-12-24": pd.Timestamp("2026-12-24 13:45", tz="America/New_York"),
    }

    for alias in ("CMEGlobex_GC", "CMEGlobex_MCL"):
        calendar = mcal.get_calendar(alias)
        schedule = calendar.schedule("2026-06-19", "2026-12-24", tz="America/New_York")

        for session, expected_close in expected_closes.items():
            actual_close = schedule.at[pd.Timestamp(session), "market_close"]
            assert actual_close == expected_close, f"{alias} {session}"


def test_2026_overrides_preserve_neighboring_year_rules():
    expected_closes = {
        "2025-06-19": pd.Timestamp("2025-06-19 14:30", tz="America/New_York"),
        "2027-06-18": pd.Timestamp("2027-06-18 14:30", tz="America/New_York"),
        "2027-07-05": pd.Timestamp("2027-07-05 14:30", tz="America/New_York"),
    }
    schedule = cal.schedule("2025-06-19", "2027-11-26", tz="America/New_York")

    for session, expected_close in expected_closes.items():
        actual_close = schedule.at[pd.Timestamp(session), "market_close"]
        assert actual_close == expected_close, session


def _assert_closes_for_crude_and_gold(expected_closes, start, end):
    for alias in ("CMEGlobex_CL", "CMEGlobex_GC"):
        schedule = mcal.get_calendar(alias).schedule(start, end, tz="America/Chicago")

        for session, expected_close in expected_closes.items():
            actual_close = schedule.at[pd.Timestamp(session), "market_close"]
            assert actual_close == expected_close, f"{alias} {session}"


# The closes below are the end of the last one-minute TRADES bar of CL, GC, HG and NG on each day:
# NinjaTrader history for 2013-2024 and Interactive Brokers history for 2024-2026.
def test_christmas_eve_closes_at_1245():
    expected_closes = {
        "2013-12-24": pd.Timestamp("2013-12-24 12:45", tz="America/Chicago"),
        "2018-12-24": pd.Timestamp("2018-12-24 12:45", tz="America/Chicago"),
        "2019-12-24": pd.Timestamp("2019-12-24 12:45", tz="America/Chicago"),
        "2020-12-24": pd.Timestamp("2020-12-24 12:45", tz="America/Chicago"),
        "2024-12-24": pd.Timestamp("2024-12-24 12:45", tz="America/Chicago"),
        "2025-12-24": pd.Timestamp("2025-12-24 12:45", tz="America/Chicago"),
        "2026-12-24": pd.Timestamp("2026-12-24 12:45", tz="America/Chicago"),
    }

    _assert_closes_for_crude_and_gold(expected_closes, "2013-12-01", "2026-12-31")


def test_friday_after_thanksgiving_closes_at_1345_from_2024():
    expected_closes = {
        "2019-11-29": pd.Timestamp("2019-11-29 12:45", tz="America/Chicago"),
        "2022-11-25": pd.Timestamp("2022-11-25 12:45", tz="America/Chicago"),
        "2023-11-24": pd.Timestamp("2023-11-24 12:45", tz="America/Chicago"),
        "2024-11-29": pd.Timestamp("2024-11-29 13:45", tz="America/Chicago"),
        "2025-11-28": pd.Timestamp("2025-11-28 13:45", tz="America/Chicago"),
        "2026-11-27": pd.Timestamp("2026-11-27 13:45", tz="America/Chicago"),
        "2027-11-26": pd.Timestamp("2027-11-26 13:45", tz="America/Chicago"),
    }

    _assert_closes_for_crude_and_gold(expected_closes, "2019-11-01", "2027-11-30")


def test_labor_day_halts_at_1330_from_2022_and_july_4_2025_closes_at_1200():
    expected_closes = {
        "2021-09-06": pd.Timestamp("2021-09-06 12:00", tz="America/Chicago"),
        "2022-09-05": pd.Timestamp("2022-09-05 13:30", tz="America/Chicago"),
        "2023-09-04": pd.Timestamp("2023-09-04 13:30", tz="America/Chicago"),
        "2025-09-01": pd.Timestamp("2025-09-01 13:30", tz="America/Chicago"),
        "2026-09-07": pd.Timestamp("2026-09-07 13:30", tz="America/Chicago"),
        "2027-09-06": pd.Timestamp("2027-09-06 13:30", tz="America/Chicago"),
        # July 4 2025 fell on a Friday: trading stopped at 12:00 and no evening session followed.
        "2023-07-04": pd.Timestamp("2023-07-04 13:30", tz="America/Chicago"),
        "2025-07-04": pd.Timestamp("2025-07-04 12:00", tz="America/Chicago"),
    }

    _assert_closes_for_crude_and_gold(expected_closes, "2021-09-01", "2027-09-30")


#########################################################################
# YEARLY TESTS BEGIN
#########################################################################
# Regression source for CME Globex Energy and Metals New Year's behavior:
# https://github.com/rsheftel/pandas_market_calendars/issues/340
# Historical CME schedule showing Jan. 3, 2011 was open after a Saturday New Year's Day:
# https://github.com/rsheftel/pandas_market_calendars/files/14588227/2011-new-years.pdf
def test_new_years_sunday_is_observed_on_monday():
    valid_days = cal.valid_days("2022-12-30", "2023-01-04")

    assert pd.Timestamp("2023-01-02", tz="UTC") not in valid_days
    assert pd.Timestamp("2023-01-03", tz="UTC") in valid_days


def test_new_years_saturday_keeps_documented_2011_sessions():
    schedule = cal.schedule("2010-12-31", "2011-01-04", tz=cal.tz)

    assert schedule.loc["2010-12-31"].market_close == pd.Timestamp("2010-12-31 15:15:00", tz=cal.tz)
    assert schedule.loc["2011-01-03"].market_open == pd.Timestamp("2011-01-02 17:00:00", tz=cal.tz)


def test_energy_and_metals_new_years_2021_closed_but_2022_monday_open():
    valid_days = cal.valid_days("2020-12-31", "2022-01-04")

    assert pd.Timestamp("2021-01-01", tz="UTC") not in valid_days
    assert pd.Timestamp("2021-12-31", tz="UTC") in valid_days
    assert pd.Timestamp("2022-01-03", tz="UTC") in valid_days


def test_2022():
    start = "2022-01-01"
    end = "2022-12-31"
    holidays = [
        pd.Timestamp("2022-04-15", tz="UTC"),  # Good Friday
        pd.Timestamp("2022-12-26", tz="UTC"),  # Christmas
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    early_closes = [
        pd.Timestamp("2022-01-17  1:30PM", tz="America/Chicago"),  # MLK
        pd.Timestamp("2022-02-21  1:30PM", tz="America/Chicago"),  # Presidents Day
        pd.Timestamp("2022-05-30  1:30PM", tz="America/Chicago"),  # Memorial Day
        pd.Timestamp("2022-06-20  1:30PM", tz="America/Chicago"),  # Juneteenth
        pd.Timestamp("2022-07-04  1:30PM", tz="America/Chicago"),  # Independence Day
        pd.Timestamp("2022-09-05  1:30PM", tz="America/Chicago"),  # Labor Day
        pd.Timestamp("2022-11-24  1:30PM", tz="America/Chicago"),  # US Thanksgiving
        pd.Timestamp("2022-11-25 12:45PM", tz="America/Chicago"),  # Friday after US Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2021():
    start = "2021-01-01"
    end = "2021-12-31"
    holidays = [
        pd.Timestamp("2021-01-01", tz="UTC"),  # New Years
        pd.Timestamp("2021-04-02", tz="UTC"),  # Good Friday
        pd.Timestamp("2021-12-24", tz="UTC"),  # Christmas
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    early_closes = [
        pd.Timestamp("2021-01-18 12:00PM", tz="America/Chicago"),  # MLK
        pd.Timestamp("2021-02-15 12:00PM", tz="America/Chicago"),  # Presidents Day
        pd.Timestamp("2021-05-31 12:00PM", tz="America/Chicago"),  # Memorial Day
        pd.Timestamp("2021-07-05 12:00PM", tz="America/Chicago"),  # Independence Day
        pd.Timestamp("2021-09-06 12:00PM", tz="America/Chicago"),  # Labor Day
        pd.Timestamp("2021-11-25 12:00PM", tz="America/Chicago"),  # US Thanksgiving
        pd.Timestamp("2021-11-26 12:45PM", tz="America/Chicago"),  # Friday after US Thanksgiving
    ]
    _test_has_early_closes(early_closes, start, end)


def test_2020():
    start = "2020-01-01"
    end = "2020-12-31"
    holidays = [
        pd.Timestamp("2020-01-01", tz="UTC"),  # New Years
        pd.Timestamp("2020-04-10", tz="UTC"),  # Good Friday
        pd.Timestamp("2020-12-25", tz="UTC"),  # Christmas
    ]
    _test_holidays(holidays, start, end)
    _test_no_special_opens(start, end)

    early_closes = [
        pd.Timestamp("2020-01-20 12:00PM", tz="America/Chicago"),  # MLK
        pd.Timestamp("2020-02-17 12:00PM", tz="America/Chicago"),  # Presidents Day
        pd.Timestamp("2020-05-25 12:00PM", tz="America/Chicago"),  # Memorial Day
        pd.Timestamp("2020-07-03 12:00PM", tz="America/Chicago"),  # Independence Day
        pd.Timestamp("2020-09-07 12:00PM", tz="America/Chicago"),  # Labor Day
        pd.Timestamp("2020-11-26 12:00PM", tz="America/Chicago"),  # US Thanksgiving
        pd.Timestamp("2020-11-27 12:45PM", tz="America/Chicago"),  # Friday after US Thanksgiving
        pd.Timestamp("2020-12-24 12:45PM", tz="America/Chicago"),  # Christmas Eve
    ]
    _test_has_early_closes(early_closes, start, end)
