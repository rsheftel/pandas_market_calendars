import datetime

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal, assert_series_equal
from zoneinfo import ZoneInfo

import pandas_market_calendars as mcal
from pandas_market_calendars.calendars.nyse import NYSEExchangeCalendar
from tests.test_market_calendar import FakeCalendar, FakeBreakCalendar, FakeETHCalendar


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
        index=pd.DatetimeIndex(["2016-07-01", "2016-07-04", "2016-07-05", "2016-07-06"]),
    )
    actual = mcal.merge_schedules([sch1, sch2], how="outer")
    assert_frame_equal(actual, expected)

    # inner join will exclude July 4th because not open for both
    expected = pd.DataFrame(
        {
            "market_open": [
                pd.Timestamp(x, tz="UTC") for x in ["2016-07-01 13:30", "2016-07-05 13:30", "2016-07-06 13:30"]
            ],
            "market_close": [
                pd.Timestamp(x, tz="UTC") for x in ["2016-07-01 02:49", "2016-07-05 02:49", "2016-07-06 02:49"]
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
    assert w[0].message.args[0] == "Merge schedules will drop the break_start and break_end from result."

    assert "break_start" not in result.columns
    assert "break_end" not in result.columns


def test_mark_session():
    cal = FakeETHCalendar()
    sched = cal.schedule("2020-01-01", "2020-02-01", market_times="all", tz=cal.tz)

    dt = mcal.date_range(
        sched,
        "1h",
        closed="left",
        periods=8,
        session={"RTH", "ETH"},
        merge_adjacent=False,
    )

    assert_series_equal(
        pd.Series(
            [
                "closed",
                "pre",
                "pre",
                "rth",
                "rth",
                "post",
                "post",
                "closed",
            ],
            index=pd.to_datetime(
                [
                    "2020-01-02 08:00:00-05:00",
                    "2020-01-02 09:00:00-05:00",
                    "2020-01-02 09:30:00-05:00",
                    "2020-01-02 10:30:00-05:00",
                    "2020-01-02 11:30:00-05:00",
                    "2020-01-02 12:30:00-05:00",
                    "2020-01-02 13:00:00-05:00",
                    "2020-01-03 08:00:00-05:00",
                ],
                utc=True,
            ).tz_convert(
                ZoneInfo("America/New_York"),
            ),
            dtype=pd.CategoricalDtype(["closed", "post", "pre", "rth"], ordered=False),
        ),
        mcal.mark_session(sched, dt),
    )

    assert_series_equal(
        pd.Series(
            [
                "pre",
                "pre",
                "rth",
                "rth",
                "post",
                "post",
                "closed",
                "pre",
            ],
            index=pd.to_datetime(
                [
                    "2020-01-02 08:00:00-05:00",
                    "2020-01-02 09:00:00-05:00",
                    "2020-01-02 09:30:00-05:00",
                    "2020-01-02 10:30:00-05:00",
                    "2020-01-02 11:30:00-05:00",
                    "2020-01-02 12:30:00-05:00",
                    "2020-01-02 13:00:00-05:00",
                    "2020-01-03 08:00:00-05:00",
                ],
                utc=True,
            ).tz_convert(
                ZoneInfo("America/New_York"),
            ),
            dtype=pd.CategoricalDtype(["closed", "post", "pre", "rth"], ordered=False),
        ),
        mcal.mark_session(sched, dt, closed="left"),
    )

    # Test Label Mapping
    mapping = {"pre": 1, "rth": 2, "post": "_post"}
    assert_series_equal(
        pd.Series(
            [
                1,
                1,
                2,
                2,
                "_post",
                "_post",
                "closed",
                1,
            ],
            index=pd.to_datetime(
                [
                    "2020-01-02 08:00:00-05:00",
                    "2020-01-02 09:00:00-05:00",
                    "2020-01-02 09:30:00-05:00",
                    "2020-01-02 10:30:00-05:00",
                    "2020-01-02 11:30:00-05:00",
                    "2020-01-02 12:30:00-05:00",
                    "2020-01-02 13:00:00-05:00",
                    "2020-01-03 08:00:00-05:00",
                ],
                utc=True,
            ).tz_convert(
                ZoneInfo("America/New_York"),
            ),
            dtype=pd.CategoricalDtype([1, 2, "_post", "closed"], ordered=False),
        ),
        mcal.mark_session(sched, dt, closed="left", label_map=mapping),
    )

    CME = mcal.get_calendar("CME_Equity")
    sched = CME.schedule("2020-01-17", "2020-01-20", market_times="all")

    # Ensure the early close on the 20th gets labeled correctly
    assert_series_equal(
        pd.Series(
            ["rth", "rth", "rth", "closed"],
            index=pd.DatetimeIndex(
                [
                    "2020-01-20 17:15:00+00:00",
                    "2020-01-20 17:30:00+00:00",
                    "2020-01-20 17:45:00+00:00",
                    "2020-01-20 18:00:00+00:00",
                ],
                dtype="datetime64[ns, UTC]",
            ),
            dtype=pd.CategoricalDtype(categories=["break", "closed", "rth"], ordered=False),
        ),
        mcal.mark_session(
            sched,
            mcal.date_range(sched, "15m", start="2020-01-20 17:00", end="2020-01-20 18:00"),
            closed="left",
        ),
    )

    sched = CME.schedule("2020-01-20", "2020-01-21", market_times="all")
    assert_series_equal(
        pd.Series(
            ["rth", "rth", "rth", "closed", "rth", "rth", "rth", "rth"],
            index=pd.DatetimeIndex(
                [
                    "2020-01-20 17:15:00+00:00",
                    "2020-01-20 17:30:00+00:00",
                    "2020-01-20 17:45:00+00:00",
                    "2020-01-20 18:00:00+00:00",
                    "2020-01-20 23:15:00+00:00",
                    "2020-01-20 23:30:00+00:00",
                    "2020-01-20 23:45:00+00:00",
                    "2020-01-21 00:00:00+00:00",
                ],
                dtype="datetime64[ns, UTC]",
            ),
            dtype=pd.CategoricalDtype(categories=["break", "closed", "rth"], ordered=False),
        ),
        mcal.mark_session(
            sched,
            mcal.date_range(sched, "15m", start="2020-01-20 17:00", end="2020-01-21 00:00"),
            closed="left",
        ),
    )


def test_mark_session_edge_case():
    # Edge case test where mark_session needs an additional schedule row because the first
    # timestamp of a given date range lands in the post market session of the day prior
    NYSE = mcal.get_calendar("NYSE")
    sched = NYSE.schedule("2015-12-25", "2016-01-05", market_times="all", tz="UTC")
    dt = pd.date_range("2015-12-31T23:00", "2016-01-01T02:00", freq="30min", tz="UTC")

    assert_series_equal(
        pd.Series(
            [
                "post",
                "post",
                "post",
                "post",
                "closed",
                "closed",
                "closed",
            ],
            index=dt,
            dtype=pd.CategoricalDtype(["closed", "post", "pre", "rth"], ordered=False),
        ),
        mcal.mark_session(sched, dt, closed="left"),
    )
