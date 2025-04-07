import datetime
import os

import pandas as pd
from zoneinfo import ZoneInfo
from pandas.testing import assert_index_equal

from pandas_market_calendars.calendars.jpx import JPXExchangeCalendar


def test_time_zone():
    assert JPXExchangeCalendar().tz == ZoneInfo("Asia/Tokyo")
    assert JPXExchangeCalendar().name == "JPX"


def test_2017_jpx_holidays():
    jpx_calendar = JPXExchangeCalendar()

    # holidays we expect
    holidays_2017 = [
        pd.Timestamp("2017-01-01", tz="UTC"),
        pd.Timestamp("2017-01-02", tz="UTC"),
        pd.Timestamp("2017-01-03", tz="UTC"),
        pd.Timestamp("2017-01-09", tz="UTC"),
        pd.Timestamp("2017-02-11", tz="UTC"),
        pd.Timestamp("2017-03-20", tz="UTC"),
        pd.Timestamp("2017-04-29", tz="UTC"),
        pd.Timestamp("2017-05-03", tz="UTC"),
        pd.Timestamp("2017-05-04", tz="UTC"),
        pd.Timestamp("2017-05-05", tz="UTC"),
        pd.Timestamp("2017-07-17", tz="UTC"),
        pd.Timestamp("2017-08-11", tz="UTC"),
        pd.Timestamp("2017-09-23", tz="UTC"),
        pd.Timestamp("2017-10-09", tz="UTC"),
        pd.Timestamp("2017-11-03", tz="UTC"),
        pd.Timestamp("2017-11-23", tz="UTC"),
        pd.Timestamp("2017-12-23", tz="UTC"),
        pd.Timestamp("2017-12-31", tz="UTC"),
    ]

    valid_days = jpx_calendar.valid_days(
        pd.Timestamp("2017-01-01"), pd.Timestamp("2017-12-31")
    )
    for session_label in holidays_2017:
        assert session_label not in valid_days


def test_2018_jpx_holidays():
    jpx_calendar = JPXExchangeCalendar()

    # holidays we expect
    holidays_2018 = [
        pd.Timestamp("2018-01-01", tz="UTC"),
        pd.Timestamp("2018-01-02", tz="UTC"),
        pd.Timestamp("2018-01-03", tz="UTC"),
        pd.Timestamp("2018-01-08", tz="UTC"),
        pd.Timestamp("2018-02-12", tz="UTC"),
        pd.Timestamp("2018-03-21", tz="UTC"),
        pd.Timestamp("2018-04-30", tz="UTC"),
        pd.Timestamp("2018-05-03", tz="UTC"),
        pd.Timestamp("2018-05-04", tz="UTC"),
        pd.Timestamp("2018-05-05", tz="UTC"),
        pd.Timestamp("2018-07-16", tz="UTC"),
        pd.Timestamp("2018-08-11", tz="UTC"),
        pd.Timestamp("2018-09-17", tz="UTC"),
        pd.Timestamp("2018-09-24", tz="UTC"),
        pd.Timestamp("2018-10-08", tz="UTC"),
        pd.Timestamp("2018-11-03", tz="UTC"),
        pd.Timestamp("2018-11-23", tz="UTC"),
        pd.Timestamp("2018-12-24", tz="UTC"),
        pd.Timestamp("2018-12-31", tz="UTC"),
    ]

    valid_days = jpx_calendar.valid_days(pd.Timestamp("2018-01-01"), pd.Timestamp("2018-12-31"))
    for session_label in holidays_2018:
        assert session_label not in valid_days


def test_jpx_2019_holidays():
    jpx_calendar = JPXExchangeCalendar()

    # holidays we expect in 2019 (calendar changes for new Emperor)
    holidays_2019 = [
        pd.Timestamp("2019-01-01", tz="UTC"),
        pd.Timestamp("2019-01-02", tz="UTC"),
        pd.Timestamp("2019-01-03", tz="UTC"),
        pd.Timestamp("2019-01-14", tz="UTC"),
        pd.Timestamp("2019-02-11", tz="UTC"),
        pd.Timestamp("2019-03-21", tz="UTC"),
        pd.Timestamp("2019-04-29", tz="UTC"),
        pd.Timestamp("2019-04-30", tz="UTC"),
        pd.Timestamp("2019-05-01", tz="UTC"),
        pd.Timestamp("2019-05-02", tz="UTC"),
        pd.Timestamp("2019-05-03", tz="UTC"),
        pd.Timestamp("2019-05-04", tz="UTC"),
        pd.Timestamp("2019-05-06", tz="UTC"),
        pd.Timestamp("2019-07-15", tz="UTC"),
        pd.Timestamp("2019-08-12", tz="UTC"),
        pd.Timestamp("2019-09-16", tz="UTC"),
        pd.Timestamp("2019-09-23", tz="UTC"),
        pd.Timestamp("2019-10-14", tz="UTC"),
        pd.Timestamp("2019-10-22", tz="UTC"),
        pd.Timestamp("2019-11-04", tz="UTC"),
        pd.Timestamp("2019-11-23", tz="UTC"),
        pd.Timestamp("2019-12-31", tz="UTC"),
    ]

    valid_days = jpx_calendar.valid_days(pd.Timestamp("2019-01-01"), pd.Timestamp("2019-12-31"))
    for session_label in holidays_2019:
        assert session_label not in valid_days


def test_jpx_2020_holidays():
    jpx_calendar = JPXExchangeCalendar()

    # holidays we expect in 2020 (calendar changes for Olympics)
    holidays_2020 = [
        pd.Timestamp("2020-01-01", tz="UTC"),
        pd.Timestamp("2020-01-02", tz="UTC"),
        pd.Timestamp("2020-01-03", tz="UTC"),
        pd.Timestamp("2020-01-13", tz="UTC"),
        pd.Timestamp("2020-02-11", tz="UTC"),
        pd.Timestamp("2020-02-24", tz="UTC"),  # from 2/23
        pd.Timestamp("2020-03-20", tz="UTC"),
        pd.Timestamp("2020-04-29", tz="UTC"),
        pd.Timestamp("2020-05-03", tz="UTC"),
        pd.Timestamp("2020-05-04", tz="UTC"),
        pd.Timestamp("2020-05-05", tz="UTC"),
        pd.Timestamp("2020-07-23", tz="UTC"),  # sea day
        pd.Timestamp("2020-07-24", tz="UTC"),  # sports day
        pd.Timestamp("2020-08-10", tz="UTC"),  # mountain day
        pd.Timestamp("2020-09-21", tz="UTC"),
        pd.Timestamp("2020-09-22", tz="UTC"),
        pd.Timestamp("2020-10-01", tz="UTC"),  # Trading system failure
        pd.Timestamp("2020-11-03", tz="UTC"),
        pd.Timestamp("2020-11-23", tz="UTC"),
        pd.Timestamp("2020-12-31", tz="UTC"),
    ]

    valid_days = jpx_calendar.valid_days(pd.Timestamp("2020-01-01"), pd.Timestamp("2020-12-31"))
    for session_label in holidays_2020:
        assert session_label not in valid_days


def test_jpx_2021_holidays():
    jpx_calendar = JPXExchangeCalendar()

    # holidays we expect in 2021 (regular calendar generation resumed)
    holidays_2021 = [
        pd.Timestamp("2021-01-01", tz="UTC"),
        pd.Timestamp("2021-01-02", tz="UTC"),
        pd.Timestamp("2021-01-03", tz="UTC"),
        pd.Timestamp("2021-01-11", tz="UTC"),
        pd.Timestamp("2021-02-11", tz="UTC"),
        pd.Timestamp("2021-02-23", tz="UTC"),
        pd.Timestamp("2021-03-20", tz="UTC"),
        pd.Timestamp("2021-04-29", tz="UTC"),
        pd.Timestamp("2021-05-03", tz="UTC"),
        pd.Timestamp("2021-05-04", tz="UTC"),
        pd.Timestamp("2021-05-05", tz="UTC"),
        pd.Timestamp("2021-07-22", tz="UTC"),  # Marine day shift for COVID
        pd.Timestamp("2021-07-23", tz="UTC"),  # Sports day shift for COVID
        pd.Timestamp("2021-08-08", tz="UTC"),  # Mountain day shift for COVID
        pd.Timestamp("2021-08-09", tz="UTC"),  # Mountain day shift for COVID
        pd.Timestamp("2021-09-20", tz="UTC"),
        pd.Timestamp("2021-09-23", tz="UTC"),
        pd.Timestamp("2021-11-03", tz="UTC"),
        pd.Timestamp("2021-11-23", tz="UTC"),
        pd.Timestamp("2021-12-31", tz="UTC"),
    ]

    valid_days = jpx_calendar.valid_days(pd.Timestamp("2021-01-01"), pd.Timestamp("2021-12-31"))
    for session_label in holidays_2021:
        assert session_label not in valid_days


def test_jpx_closes_at_lunch():
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(
        start_date=datetime.datetime(2015, 1, 14, tzinfo=ZoneInfo("Asia/Tokyo")),
        end_date=datetime.datetime(2015, 1, 16, tzinfo=ZoneInfo("Asia/Tokyo")),
    )

    assert jpx_calendar.open_at_time(
        schedule=jpx_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 11, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
    )

    assert not jpx_calendar.open_at_time(
        schedule=jpx_schedule,
        timestamp=datetime.datetime(2015, 1, 14, 12, 0, tzinfo=ZoneInfo("Asia/Tokyo")),
    )


def test_jpx_correctly_counts_jpx_autumn_equinox():
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(start_date="2016-09-01", end_date="2019-09-30")
    assert pd.Timestamp("2016-09-22") not in jpx_schedule.index
    assert pd.Timestamp("2016-09-23") in jpx_schedule.index

    assert pd.Timestamp("2017-09-23") not in jpx_schedule.index  # EQUINOX Saturday
    assert pd.Timestamp("2017-09-24") not in jpx_schedule.index  # Sunday
    assert pd.Timestamp("2017-09-25") in jpx_schedule.index  # Monday

    assert pd.Timestamp("2018-09-22") not in jpx_schedule.index  # Saturday
    assert pd.Timestamp("2018-09-23") not in jpx_schedule.index  # EQUINOX Sunday
    assert pd.Timestamp("2018-09-24") not in jpx_schedule.index  # Equinox OBS

    assert pd.Timestamp("2019-09-22") not in jpx_schedule.index  # Sunday
    assert pd.Timestamp("2019-09-23") not in jpx_schedule.index  # EQUINOX
    assert pd.Timestamp("2019-09-24") in jpx_schedule.index  # Monday


def test_jpx_correctly_counts_jpx_vernal_equinox():
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(start_date="2017-03-01", end_date="2019-09-30")

    assert pd.Timestamp("2017-03-20") not in jpx_schedule.index
    assert pd.Timestamp("2017-03-21") in jpx_schedule.index

    assert pd.Timestamp("2018-03-21") not in jpx_schedule.index

    assert pd.Timestamp("2019-03-21") not in jpx_schedule.index
    assert pd.Timestamp("2019-03-20") in jpx_schedule.index


def test_jpx_trading_days_since_1949(request):
    """
    Perform a full comparison of all known weekday trading days from 1949-05-16 to 2019-05-31 and
    make sure that it matches.
    """
    # get the expected dates from the csv file
    expected = pd.read_csv(
        os.path.join(request.fspath.dirname, "data", "jpx_open_weekdays_since_1949.csv"),
        index_col=0,
        parse_dates=True,
    ).index
    expected.name = None

    # calculated expected going direct to the underlying regular and ad_hoc calendars
    jpx_calendar = JPXExchangeCalendar()
    start_date = expected[0]
    end_date = expected[-1]
    reg_holidays = jpx_calendar.regular_holidays.holidays(start_date, end_date)
    adhoc_dates = map(lambda dt: dt.tz_localize(None), jpx_calendar.adhoc_holidays)
    adhoc_index = pd.DatetimeIndex(adhoc_dates).sort_values()
    slice_locs = adhoc_index.slice_locs(start_date, end_date)
    adhoc_holidays = adhoc_index[slice_locs[0] : slice_locs[1]]
    holidays = reg_holidays
    holidays = holidays.append(adhoc_holidays)
    holidays = holidays.sort_values().unique()
    day_generator = pd.offsets.CustomBusinessDay(holidays=holidays)
    actual = pd.date_range(start_date, end_date, freq=day_generator)

    assert_index_equal(expected, actual)


def test_jpx_change_in_market_close():
    """
    The market close of Japan changed from 3:00 PM to 3:30 PM on November 5, 2024, make sure the
    calendar reflects this change.
    """
    jpx_calendar = JPXExchangeCalendar()
    jpx_schedule = jpx_calendar.schedule(start_date="2024-10-28", end_date="2024-11-08")

    business_dates_before_change = [
        "2024-10-28",
        "2024-10-29",
        "2024-10-30",
        "2024-10-31",
        "2024-11-01",
    ]

    business_dates_after_change = [
        "2024-11-05",
        "2024-11-06",
        "2024-11-07",
        "2024-11-08",
    ]

    for date in business_dates_before_change:
        assert jpx_schedule.loc[date, "market_close"] == pd.Timestamp(f"{date} 15:00", tz="Asia/Tokyo")

    for date in business_dates_after_change:
        assert jpx_schedule.loc[date, "market_close"] == pd.Timestamp(f"{date} 15:30", tz="Asia/Tokyo")
