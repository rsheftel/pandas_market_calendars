import datetime

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar
from tests.test_market_calendar import FakeCalendar, FakeBreakCalendar


def test_get_calendar():
    assert isinstance(mcal.get_calendar("NYSE"), NYSEExchangeCalendar)
    cal = mcal.get_calendar("NYSE", datetime.time(10, 0), datetime.time(14, 30))
    assert isinstance(cal, NYSEExchangeCalendar)
    assert cal.open_time == datetime.time(10, 0)
    assert cal.close_time == datetime.time(14, 30)

    # confirm that import works properly
    _ = mcal.get_calendar("CME_Equity")


def test_get_calendar_names():
    assert "ASX" in mcal.get_calendar_names()


def test_merge_schedules():
    cal1 = FakeCalendar()
    cal2 = NYSEExchangeCalendar()

    # cal1 is open on 2016-07-04 and cal2 is not
    sch1 = cal1.schedule("2016-07-01", "2016-07-06")
    sch2 = cal2.schedule("2016-07-01", "2016-07-06")

    # outer join will include July 4th and have
    expected = pd.DataFrame(
        {
            "market_open": [
                pd.Timestamp(x, tz="UTC")
                for x in [
                    "2016-07-01 02:13",
                    "2016-07-04 02:13",
                    "2016-07-05 02:13",
                    "2016-07-06 02:13",
                ]
            ],
            "market_close": [
                pd.Timestamp(x, tz="UTC")
                for x in [
                    "2016-07-01 20:00",
                    "2016-07-04 02:49",
                    "2016-07-05 20:00",
                    "2016-07-06 20:00",
                ]
            ],
        },
        columns=["market_open", "market_close"],
        index=pd.DatetimeIndex(
            ["2016-07-01", "2016-07-04", "2016-07-05", "2016-07-06"]
        ),
    )
    actual = mcal.merge_schedules([sch1, sch2], how="outer")
    assert_frame_equal(actual, expected)

    # inner join will exclude July 4th because not open for both
    expected = pd.DataFrame(
        {
            "market_open": [
                pd.Timestamp(x, tz="UTC")
                for x in ["2016-07-01 13:30", "2016-07-05 13:30", "2016-07-06 13:30"]
            ],
            "market_close": [
                pd.Timestamp(x, tz="UTC")
                for x in ["2016-07-01 02:49", "2016-07-05 02:49", "2016-07-06 02:49"]
            ],
        },
        columns=["market_open", "market_close"],
        index=pd.DatetimeIndex(["2016-07-01", "2016-07-05", "2016-07-06"]),
    )
    actual = mcal.merge_schedules([sch1, sch2], how="inner")
    assert_frame_equal(actual, expected)

    # joining more than two calendars works correctly
    actual = mcal.merge_schedules([sch1, sch1, sch1], how="inner")
    assert_frame_equal(actual, sch1)

    with pytest.raises(ValueError):
        mcal.merge_schedules([sch1, sch2], how="left")


def test_merge_schedules_w_break():
    # this currently does not work as all breaks are lost
    cal = FakeCalendar()
    cal_breaks = FakeBreakCalendar()

    schedule = cal.schedule("2016-12-20", "2016-12-30")
    schedule_breaks = cal_breaks.schedule("2016-12-20", "2016-12-30")

    with pytest.warns(Warning) as w:
        result = mcal.merge_schedules([schedule, schedule_breaks])
    assert (
        w[0].message.args[0]
        == "Merge schedules will drop the break_start and break_end from result."
    )

    assert "break_start" not in result.columns
    assert "break_end" not in result.columns
