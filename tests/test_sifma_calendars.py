import pandas as pd
from zoneinfo import ZoneInfo
from pandas.testing import assert_index_equal

from pandas_market_calendars.calendars.sifma import (
    SIFMAUSExchangeCalendar,
    SIFMAUKExchangeCalendar,
    SIFMAJPExchangeCalendar,
)


#########################################################################
# HELPER FUNCTIONS
#########################################################################
def _test_holidays(cal, holidays, start, end):
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


def _test_no_special_opens(cal, start, end):
    assert len(cal.late_opens(cal.schedule(start, end))) == 0


def _test_no_special_closes(cal, start, end):
    assert len(cal.early_closes(cal.schedule(start, end))) == 0


def _test_no_special_opens_closes(cal, start, end):
    _test_no_special_opens(cal, start, end)
    _test_no_special_closes(cal, start, end)


def _test_verify_late_open_time(schedule, timestamp):
    date = pd.Timestamp(pd.Timestamp(timestamp).tz_convert("UTC").date())
    if date in schedule.index:
        return schedule.at[date, "market_open"] == timestamp
    else:
        return False


def _test_has_late_opens(cal, late_opens, start, end):
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


def _test_has_early_closes(cal, early_closes, start, end):
    schedule = cal.schedule(start, end)
    expected = cal.early_closes(schedule)
    assert len(expected) == len(early_closes)
    for ts in early_closes:
        assert _test_verify_early_close_time(schedule, ts) is True


#########################################################################
# US TESTS
#########################################################################
sifma_us = SIFMAUSExchangeCalendar()


def test_us_time_zone():
    assert sifma_us.tz == ZoneInfo("America/New_York")
    assert sifma_us.name == "SIFMA_US"


def test_us_open_time_tz():
    assert sifma_us.open_time.tzinfo == sifma_us.tz


def test_us_close_time_tz():
    assert sifma_us.close_time.tzinfo == sifma_us.tz


def test_us_weekmask():
    assert sifma_us.weekmask == "Mon Tue Wed Thu Fri"


def test_us_2025():
    start = "2025-01-01"
    end = "2025-12-31"
    holidays = [
        pd.Timestamp("2025-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2025-01-20", tz="UTC"),  # MLK
        pd.Timestamp("2025-02-17", tz="UTC"),  # Presidents Day
        pd.Timestamp("2025-04-18", tz="UTC"),  # Good Friday (NOT first Friday)
        pd.Timestamp("2025-05-26", tz="UTC"),  # Memorial Day
        pd.Timestamp("2025-06-19", tz="UTC"),  # Juneteenth
        pd.Timestamp("2025-07-04", tz="UTC"),  # Independence Day
        pd.Timestamp("2025-09-01", tz="UTC"),  # Labor Day
        pd.Timestamp("2025-10-13", tz="UTC"),  # Columbus Day
        pd.Timestamp("2025-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2025-11-27", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2025-12-25", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp(
            "2025-04-17 2:00PM", tz="America/New_York"
        ),  # Day before Good Friday (2pm because GF is full holiday)
        pd.Timestamp("2025-05-23 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2025-07-03 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2025-11-28 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2025-12-24 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2025-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2024():
    start = "2024-01-01"
    end = "2024-12-31"
    holidays = [
        pd.Timestamp("2024-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2024-01-15", tz="UTC"),  # MLK
        pd.Timestamp("2024-02-19", tz="UTC"),  # Presidents Day
        pd.Timestamp("2024-03-29", tz="UTC"),  # Good Friday (NOT first Friday)
        pd.Timestamp("2024-05-27", tz="UTC"),  # Memorial Day
        pd.Timestamp("2024-06-19", tz="UTC"),  # Juneteenth
        pd.Timestamp("2024-07-04", tz="UTC"),  # Independence Day
        pd.Timestamp("2024-09-02", tz="UTC"),  # Labor Day
        pd.Timestamp("2024-10-14", tz="UTC"),  # Columbus Day
        pd.Timestamp("2024-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2024-11-28", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2024-12-25", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp(
            "2024-03-28 2:00PM", tz="America/New_York"
        ),  # Day before Good Friday (2pm because GF is full holiday)
        pd.Timestamp("2024-05-24 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2024-07-03 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2024-11-29 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2024-12-24 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2024-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2023():
    start = "2023-01-01"
    end = "2023-12-31"
    # Note: Good Friday 2023-04-07 IS the first Friday -> 12pm early close
    holidays = [
        pd.Timestamp("2023-01-02", tz="UTC"),  # New Year's Day
        pd.Timestamp("2023-01-16", tz="UTC"),  # MLK
        pd.Timestamp("2023-02-20", tz="UTC"),  # Presidents Day
        # Good Friday is NOT a full holiday
        pd.Timestamp("2023-05-29", tz="UTC"),  # Memorial Day
        pd.Timestamp("2023-06-19", tz="UTC"),  # Juneteenth
        pd.Timestamp("2023-07-04", tz="UTC"),  # Independence Day
        pd.Timestamp("2023-09-04", tz="UTC"),  # Labor Day
        pd.Timestamp("2023-10-09", tz="UTC"),  # Columbus Day
        pd.Timestamp("2023-11-23", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2023-12-25", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2023-04-07 12:00PM", tz="America/New_York"),  # Good Friday (12pm because it's the first Friday)
        # No early close the day before Good Friday
        pd.Timestamp("2023-05-26 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2023-07-03 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2023-11-24 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2023-12-22 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2023-12-29 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2022():
    start = "2022-01-01"
    end = "2022-12-31"
    # Note: Good Friday 2022-04-15 is NOT the first Friday -> full holiday
    holidays = [
        pd.Timestamp("2022-01-17", tz="UTC"),  # MLK
        pd.Timestamp("2022-02-21", tz="UTC"),  # Presidents Day
        pd.Timestamp("2022-04-15", tz="UTC"),  # Good Friday (Full Holiday)
        pd.Timestamp("2022-05-30", tz="UTC"),  # Memorial Day
        pd.Timestamp("2022-06-20", tz="UTC"),  # Juneteenth
        pd.Timestamp("2022-07-04", tz="UTC"),  # Independence Day
        pd.Timestamp("2022-09-05", tz="UTC"),  # Labor Day
        pd.Timestamp("2022-10-10", tz="UTC"),  # Columbus Day
        pd.Timestamp("2022-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2022-11-24", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2022-12-26", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp(
            "2022-04-14 2:00PM", tz="America/New_York"
        ),  # Day before Good Friday (2pm because GF is full holiday)
        pd.Timestamp("2022-05-27 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2022-07-01 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2022-11-25 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2022-12-23 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2022-12-30 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2021():
    start = "2021-01-01"
    end = "2021-12-31"
    # Note: Good Friday 2021-04-02 IS the first Friday -> 12pm early close
    holidays = [
        pd.Timestamp("2021-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2021-01-18", tz="UTC"),  # MLK
        pd.Timestamp("2021-02-15", tz="UTC"),  # Presidents Day
        # Good Friday is NOT a full holiday
        pd.Timestamp("2021-05-31", tz="UTC"),  # Memorial Day
        # Juneteenth not observed by SIFMA in 2021
        pd.Timestamp("2021-07-05", tz="UTC"),  # Independence Day observed
        pd.Timestamp("2021-09-06", tz="UTC"),  # Labor Day
        pd.Timestamp("2021-10-11", tz="UTC"),  # Columbus Day
        pd.Timestamp("2021-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2021-11-25", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2021-12-24", tz="UTC"),  # Christmas observed
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2021-04-02 12:00PM", tz="America/New_York"),  # Good Friday (12pm because it's the first Friday)
        # No early close the day before Good Friday
        pd.Timestamp("2021-05-28 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2021-07-02 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2021-11-26 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2021-12-23 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2021-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2020():
    start = "2020-01-01"
    end = "2020-12-31"
    holidays = [
        pd.Timestamp("2020-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2020-01-20", tz="UTC"),  # MLK
        pd.Timestamp("2020-02-17", tz="UTC"),  # Presidents Day
        pd.Timestamp("2020-04-10", tz="UTC"),  # Good Friday
        pd.Timestamp("2020-05-25", tz="UTC"),  # Memorial Day
        pd.Timestamp("2020-07-03", tz="UTC"),  # Independence Day
        pd.Timestamp("2020-09-07", tz="UTC"),  # Labor Day
        pd.Timestamp("2020-10-12", tz="UTC"),  # Columbus Day
        pd.Timestamp("2020-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2020-11-26", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2020-12-25", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2020-04-09 2:00PM", tz="America/New_York"),  # Day before Good Friday
        pd.Timestamp("2020-05-22 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2020-07-02 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2020-11-27 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2020-12-24 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2020-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2019():
    start = "2019-01-01"
    end = "2019-12-31"
    holidays = [
        pd.Timestamp("2019-01-01", tz="UTC"),
        pd.Timestamp("2019-01-21", tz="UTC"),
        pd.Timestamp("2019-02-18", tz="UTC"),
        pd.Timestamp("2019-04-19", tz="UTC"),
        pd.Timestamp("2019-05-27", tz="UTC"),
        pd.Timestamp("2019-07-04", tz="UTC"),
        pd.Timestamp("2019-09-02", tz="UTC"),
        pd.Timestamp("2019-10-14", tz="UTC"),
        pd.Timestamp("2019-11-11", tz="UTC"),
        pd.Timestamp("2019-11-28", tz="UTC"),
        pd.Timestamp("2019-12-25", tz="UTC"),
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2019-04-18 2:00PM", tz="America/New_York"),  # Day before Good Friday
        pd.Timestamp("2019-05-24 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2019-07-03 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2019-11-29 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2019-12-24 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2019-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2026():
    start = "2026-01-01"
    end = "2026-12-31"
    # Note: Good Friday 2026-04-03 IS the first Friday -> 12pm early close
    holidays = [
        pd.Timestamp("2026-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2026-01-19", tz="UTC"),  # MLK
        pd.Timestamp("2026-02-16", tz="UTC"),  # Presidents Day
        # Good Friday is NOT a full holiday
        pd.Timestamp("2026-05-25", tz="UTC"),  # Memorial Day
        pd.Timestamp("2026-06-19", tz="UTC"),  # Juneteenth
        pd.Timestamp("2026-07-03", tz="UTC"),  # Independence Day observed
        pd.Timestamp("2026-09-07", tz="UTC"),  # Labor Day
        pd.Timestamp("2026-10-12", tz="UTC"),  # Columbus Day
        pd.Timestamp("2026-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2026-11-26", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2026-12-25", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp("2026-04-03 12:00PM", tz="America/New_York"),  # Good Friday (12pm because it's the first Friday)
        # No early close the day before Good Friday
        pd.Timestamp("2026-05-22 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2026-07-02 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2026-11-27 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2026-12-24 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2026-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


def test_us_2027():
    start = "2027-01-01"
    end = "2027-12-31"
    # Note: Good Friday 2027-03-26 is NOT the first Friday -> full holiday
    holidays = [
        pd.Timestamp("2027-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2027-01-18", tz="UTC"),  # MLK
        pd.Timestamp("2027-02-15", tz="UTC"),  # Presidents Day
        pd.Timestamp("2027-03-26", tz="UTC"),  # Good Friday (Full Holiday)
        pd.Timestamp("2027-05-31", tz="UTC"),  # Memorial Day
        pd.Timestamp("2027-06-18", tz="UTC"),  # Juneteenth observed
        pd.Timestamp("2027-07-05", tz="UTC"),  # Independence Day observed
        pd.Timestamp("2027-09-06", tz="UTC"),  # Labor Day
        pd.Timestamp("2027-10-11", tz="UTC"),  # Columbus Day
        pd.Timestamp("2027-11-11", tz="UTC"),  # Veterans Day
        pd.Timestamp("2027-11-25", tz="UTC"),  # Thanksgiving
        pd.Timestamp("2027-12-24", tz="UTC"),  # Christmas observed
    ]
    _test_holidays(sifma_us, holidays, start, end)
    _test_no_special_opens(sifma_us, start, end)

    # early closes we expect:
    early_closes = [
        pd.Timestamp(
            "2027-03-25 2:00PM", tz="America/New_York"
        ),  # Day before Good Friday (2pm because GF is full holiday)
        pd.Timestamp("2027-05-28 2:00PM", tz="America/New_York"),  # Day before Memorial Day
        pd.Timestamp("2027-07-02 2:00PM", tz="America/New_York"),  # Day before Independence Day
        pd.Timestamp("2027-11-26 2:00PM", tz="America/New_York"),  # Day after Thanksgiving
        pd.Timestamp("2027-12-23 2:00PM", tz="America/New_York"),  # Day before Christmas
        pd.Timestamp("2027-12-31 2:00PM", tz="America/New_York"),  # New Year's Eve
    ]
    _test_has_early_closes(sifma_us, early_closes, start, end)


#########################################################################
# UK TESTS
#########################################################################
sifma_uk = SIFMAUKExchangeCalendar()


def test_uk_time_zone():
    assert sifma_uk.tz == ZoneInfo("Europe/London")
    assert sifma_uk.name == "SIFMA_UK"


def test_uk_open_time_tz():
    assert sifma_uk.open_time.tzinfo == sifma_uk.tz


def test_uk_close_time_tz():
    assert sifma_uk.close_time.tzinfo == sifma_uk.tz


def test_uk_weekmask():
    assert sifma_uk.weekmask == "Mon Tue Wed Thu Fri"


def test_uk_2023():
    start = "2023-01-01"
    end = "2023-12-31"
    holidays = [
        pd.Timestamp("2023-01-02", tz="UTC"),  # New Year's Day
        pd.Timestamp("2023-01-16", tz="UTC"),  # MLK
        pd.Timestamp("2023-02-20", tz="UTC"),  # US Presidents Day
        pd.Timestamp("2023-04-07", tz="UTC"),  # Good Friday
        pd.Timestamp("2023-04-10", tz="UTC"),  # Easter Monday
        pd.Timestamp("2023-05-01", tz="UTC"),  # May Day
        pd.Timestamp("2023-05-29", tz="UTC"),  # Memorial Day + Spring Bank Holiday
        pd.Timestamp("2023-06-19", tz="UTC"),  # Juneteenth
        pd.Timestamp("2023-07-04", tz="UTC"),  # US Independence Day
        pd.Timestamp("2023-08-28", tz="UTC"),  # UK Summer Bank Holiday
        pd.Timestamp("2023-09-04", tz="UTC"),  # US Labor Day
        pd.Timestamp("2023-10-09", tz="UTC"),  # US Columbus Day
        pd.Timestamp("2023-11-23", tz="UTC"),  # US Thanksgiving
        pd.Timestamp("2023-12-25", tz="UTC"),  # Christmas
        pd.Timestamp("2023-12-26", tz="UTC"),  # Boxing Day
    ]
    _test_holidays(sifma_uk, holidays, start, end)
    _test_no_special_opens_closes(sifma_uk, start, end)


def test_uk_2022():
    start = "2022-01-01"
    end = "2022-12-31"
    holidays = [
        pd.Timestamp("2022-01-03", tz="UTC"),  # New Year's Day
        pd.Timestamp("2022-01-17", tz="UTC"),  # MLK
        pd.Timestamp("2022-02-21", tz="UTC"),  # US Presidents Day
        pd.Timestamp("2022-04-15", tz="UTC"),  # Good Friday
        pd.Timestamp("2022-04-18", tz="UTC"),  # Easter Monday
        pd.Timestamp("2022-05-02", tz="UTC"),  # May Day
        pd.Timestamp("2022-05-30", tz="UTC"),  # Memorial Day
        pd.Timestamp("2022-06-02", tz="UTC"),  # Spring Bank Holiday
        pd.Timestamp("2022-06-03", tz="UTC"),  # Platinum Jubilee
        pd.Timestamp("2022-06-20", tz="UTC"),  # Juneteenth
        pd.Timestamp("2022-07-04", tz="UTC"),  # US Independence Day
        pd.Timestamp("2022-08-29", tz="UTC"),  # UK Summer Bank Holiday
        pd.Timestamp("2022-09-05", tz="UTC"),  # US Labor Day
        pd.Timestamp("2022-10-10", tz="UTC"),  # US Columbus Day
        pd.Timestamp("2022-11-11", tz="UTC"),  # US Vetrans Day
        pd.Timestamp("2022-11-24", tz="UTC"),  # US Thanksgiving
        pd.Timestamp("2022-12-26", tz="UTC"),  # Boxing Day
        pd.Timestamp("2022-12-27", tz="UTC"),  # Christmas
    ]
    _test_holidays(sifma_uk, holidays, start, end)
    _test_no_special_opens_closes(sifma_uk, start, end)


def test_uk_2021():
    start = "2021-01-01"
    end = "2021-12-31"
    holidays = [
        pd.Timestamp("2021-01-01", tz="UTC"),  # New Year's Day
        pd.Timestamp("2021-01-18", tz="UTC"),  # MLK
        pd.Timestamp("2021-02-15", tz="UTC"),  # US Presidents Day
        pd.Timestamp("2021-04-02", tz="UTC"),  # Good Friday
        pd.Timestamp("2021-04-05", tz="UTC"),  # Easter Monday
        pd.Timestamp("2021-05-03", tz="UTC"),  # May Day
        pd.Timestamp("2021-05-31", tz="UTC"),  # Memorial Day + Spring Bank Holiday
        pd.Timestamp("2021-07-05", tz="UTC"),  # US Independence Day
        pd.Timestamp("2021-08-30", tz="UTC"),  # UK Summer Bank Holiday
        pd.Timestamp("2021-09-06", tz="UTC"),  # US Labor Day
        pd.Timestamp("2021-10-11", tz="UTC"),  # US Columbus Day
        pd.Timestamp("2021-11-11", tz="UTC"),  # US Vetrans Day
        pd.Timestamp("2021-11-25", tz="UTC"),  # US Thanksgiving
        pd.Timestamp("2021-12-24", tz="UTC"),  # Friday Christmas Eve
        pd.Timestamp("2021-12-27", tz="UTC"),  # Christmas
        pd.Timestamp("2021-12-28", tz="UTC"),  # Boxing Day
    ]
    _test_holidays(sifma_uk, holidays, start, end)
    _test_no_special_opens_closes(sifma_uk, start, end)


#########################################################################
# Japan TESTS
#########################################################################
sifma_jp = SIFMAJPExchangeCalendar()


def test_jp_time_zone():
    assert sifma_jp.tz == ZoneInfo("Asia/Tokyo")
    assert sifma_jp.name == "SIFMA_JP"


def test_jp_open_time_tz():
    assert sifma_jp.open_time.tzinfo == sifma_jp.tz


def test_jp_close_time_tz():
    assert sifma_jp.close_time.tzinfo == sifma_jp.tz


def test_jp_weekmask():
    assert sifma_jp.weekmask == "Mon Tue Wed Thu Fri"


def test_jp_2022():
    start = "2022-01-01"
    end = "2022-12-31"
    holidays = [
        pd.Timestamp("2022-01-03", tz="UTC"),  # New Year's Day
        pd.Timestamp("2022-01-10", tz="UTC"),  # Japan Coming of Age Day
        pd.Timestamp("2022-01-17", tz="UTC"),  # US MLK
        pd.Timestamp("2022-02-11", tz="UTC"),  # Japan National Foundation Day
        pd.Timestamp("2022-02-21", tz="UTC"),  # US Presidents Day
        pd.Timestamp("2022-02-23", tz="UTC"),  # Japan Emporer's Birthday
        pd.Timestamp("2022-03-21", tz="UTC"),  # Japan Vernal Equinox
        pd.Timestamp("2022-04-15", tz="UTC"),  # UK Good Friday
        pd.Timestamp("2022-04-18", tz="UTC"),  # UK Easter Monday
        pd.Timestamp("2022-04-29", tz="UTC"),  # Japan Showa Day
        pd.Timestamp("2022-05-03", tz="UTC"),  # Japan Constitution Day
        pd.Timestamp("2022-05-04", tz="UTC"),  # Japan Greenery Day
        pd.Timestamp("2022-05-05", tz="UTC"),  # Japan Children's Day
        pd.Timestamp("2022-05-30", tz="UTC"),  # US Memorial Day
        pd.Timestamp("2022-06-02", tz="UTC"),  # UK Spring Bank Holiday
        pd.Timestamp("2022-06-03", tz="UTC"),  # UK Platinum Jubilee
        pd.Timestamp("2022-06-20", tz="UTC"),  # Juneteenth
        pd.Timestamp("2022-07-04", tz="UTC"),  # US Independence Day
        pd.Timestamp("2022-07-18", tz="UTC"),  # Japan Marine Day
        pd.Timestamp("2022-08-11", tz="UTC"),  # Japan Mountain Day
        pd.Timestamp("2022-08-29", tz="UTC"),  # UK Summer Bank Holiday
        pd.Timestamp("2022-09-05", tz="UTC"),  # US Labor Day
        pd.Timestamp("2022-09-19", tz="UTC"),  # Japan Respect-for-the-Aged Day
        pd.Timestamp("2022-09-23", tz="UTC"),  # Japan Autumnal Equinox
        pd.Timestamp("2022-10-10", tz="UTC"),  # Japan Health and Sports Day
        pd.Timestamp("2022-11-03", tz="UTC"),  # Japan Culture Day
        pd.Timestamp("2022-11-11", tz="UTC"),  # US Vetrans Day
        pd.Timestamp("2022-11-23", tz="UTC"),  # Japan Labour Thanksgiving Day
        pd.Timestamp("2022-11-24", tz="UTC"),  # US Thanksgiving
        pd.Timestamp("2022-12-26", tz="UTC"),  # Boxing Day
    ]
    _test_holidays(sifma_jp, holidays, start, end)
    _test_no_special_opens(sifma_jp, start, end)

    early_closes = [
        pd.Timestamp("2022-05-02 3:00PM", tz="Asia/Tokyo"),  # UK May Day
        pd.Timestamp("2022-12-27 3:00PM", tz="Asia/Tokyo"),  # UK Christmas Day
    ]
    _test_has_early_closes(sifma_jp, early_closes, start, end)


if __name__ == "__main__":
    for ref, obj in locals().copy().items():
        if ref.startswith("test_"):
            print("running ", ref)
            obj()
