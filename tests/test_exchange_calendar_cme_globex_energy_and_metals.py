import pandas as pd
from pandas.testing import assert_index_equal
from zoneinfo import ZoneInfo

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
        pd.Timestamp("2022-09-05 12:00PM", tz="America/Chicago"),  # Labor Day
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
    ]
    _test_has_early_closes(early_closes, start, end)
