import datetime

import pandas as pd
import pytest
from pandas.testing import assert_index_equal

import pandas_market_calendars as mcal
from tests.test_market_calendar import FakeCalendar, FakeBreakCalendar

from pandas_market_calendars.calendar_utils import (
    MissingSessionWarning,
    _make_session_list,
    DisappearingSessionWarning,
    OverlappingSessionWarning,
    filter_date_range_warnings,
    missing_columns,
    missing_sessions,
)


def test_date_range_exceptions():
    cal = FakeCalendar(open_time=datetime.time(9), close_time=datetime.time(11, 30))
    schedule = cal.schedule("2021-01-05", "2021-01-05")

    # invalid closed argument
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, "15min", closed="righ")
    assert e.exconly() == "ValueError: closed must be 'left', 'right', 'both' or None."

    # invalid force_close argument
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, "15min", force_close="True")
    assert e.exconly() == "ValueError: force_close must be True, False or None."

    # close_time is before open_time
    schedule = pd.DataFrame(
        [["2020-01-01 12:00:00+00:00", "2020-01-01 11:00:00+00:00"]],
        index=["2020-01-01"],
        columns=["market_open", "market_close"],
    )
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, "15min", closed="right", force_close=True)
    assert (
        e.exconly()
        == "ValueError: Desired Sessions from the Schedule contain rows where session start < session end, "
        "please correct the schedule"
    )

    # Overlap -
    # the end of the last bar goes over the next start time
    bcal = FakeBreakCalendar()
    bschedule = bcal.schedule("2021-01-05", "2021-01-05")

    # ** Was a Value Error, Was Changed to a Warning. Escalate and test**
    filter_date_range_warnings("error", OverlappingSessionWarning)

    with pytest.raises(OverlappingSessionWarning) as e1:
        # this frequency overlaps
        mcal.date_range(bschedule, "2h", closed="right", force_close=None)
    # this doesn't
    mcal.date_range(bschedule, "1h", closed="right", force_close=None)

    with pytest.raises(OverlappingSessionWarning) as e2:
        mcal.date_range(bschedule, "2h", closed="both", force_close=None)
    mcal.date_range(bschedule, "1h", closed="right", force_close=None)

    with pytest.raises(OverlappingSessionWarning) as e3:
        mcal.date_range(bschedule, "2h", closed=None, force_close=None)
    mcal.date_range(bschedule, "1h", closed="right", force_close=None)

    for e in (e1, e2, e3):
        assert (
            e.exconly()
            == "pandas_market_calendars.calendar_utils.OverlappingSessionWarning: "
            "The desired frequency results in date_range() generating overlapping sessions. "
            "This can happen when the timestep is larger than a session, or when "
            "merge_session = False and a session is not evenly divisible by the timestep. "
            "The overlapping timestep can be deleted with force_close = True or False"
        )

    # de-escalate and re-test
    filter_date_range_warnings("default", OverlappingSessionWarning)

    with pytest.warns(OverlappingSessionWarning) as w1:
        mcal.date_range(bschedule, "2h", closed="right", force_close=None)

    with pytest.warns(OverlappingSessionWarning) as w2:
        mcal.date_range(bschedule, "2h", closed="both", force_close=None)

    with pytest.warns(OverlappingSessionWarning) as w3:
        mcal.date_range(bschedule, "2h", closed=None, force_close=None)

    assert all([w1, w2, w3])

    try:
        # should all be fine, since force_close cuts the overlapping interval
        mcal.date_range(bschedule, "2h", closed="right", force_close=True)

        with pytest.warns(
            DisappearingSessionWarning
        ):  # should also warn about lost sessions
            mcal.date_range(bschedule, "2h", closed="right", force_close=False)

        mcal.date_range(bschedule, "2h", closed="both", force_close=True)
        mcal.date_range(bschedule, "2h", closed="both", force_close=False)
        # closed = "left" should never be a problem since it won't go outside market hours anyway
        mcal.date_range(bschedule, "2h", closed="left", force_close=True)
        mcal.date_range(bschedule, "2h", closed="left", force_close=False)
        mcal.date_range(bschedule, "2h", closed="left", force_close=None)
    except ValueError as e:
        pytest.fail(f"Unexpected Error: \n{e}")


@pytest.mark.parametrize("tz", ["America/New_York", "Asia/Ulaanbaatar", "UTC"])
def test_date_range_permutations(tz):
    # open_time = 9, close_time = 11.30, freq = "1h"
    cal = FakeCalendar(open_time=datetime.time(9), close_time=datetime.time(11, 30))
    schedule = cal.schedule("2021-01-05", "2021-01-05", tz=tz)

    # result         matching values for:   closed force_close
    # 9 10 11        left False/ left None/ both False/ None False
    expected = pd.DatetimeIndex(
        [
            "2021-01-05 01:00:00+00:00",
            "2021-01-05 02:00:00+00:00",
            "2021-01-05 03:00:00+00:00",
        ],
        tz=tz,
    )
    actual = mcal.date_range(schedule, "1h", closed="left", force_close=False)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1h", closed="left", force_close=None)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1h", closed="both", force_close=False)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1h", closed=None, force_close=False)
    assert_index_equal(actual, expected)

    # 9 10 11 11.30  left True/ both True/ None True
    expected = pd.DatetimeIndex(
        [
            "2021-01-05 01:00:00+00:00",
            "2021-01-05 02:00:00+00:00",
            "2021-01-05 03:00:00+00:00",
            "2021-01-05 03:30:00+00:00",
        ],
        tz=tz,
    )
    actual = mcal.date_range(schedule, "1h", closed="left", force_close=True)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1h", closed="both", force_close=True)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1h", closed=None, force_close=True)
    assert_index_equal(actual, expected)

    # 10 11          right False
    expected = pd.DatetimeIndex(
        ["2021-01-05 02:00:00+00:00", "2021-01-05 03:00:00+00:00"], tz=tz
    )
    actual = mcal.date_range(schedule, "1h", closed="right", force_close=False)
    assert_index_equal(actual, expected)

    # 10 11 11.30    right True
    expected = pd.DatetimeIndex(
        [
            "2021-01-05 02:00:00+00:00",
            "2021-01-05 03:00:00+00:00",
            "2021-01-05 03:30:00+00:00",
        ],
        tz=tz,
    )
    actual = mcal.date_range(schedule, "1h", closed="right", force_close=True)
    assert_index_equal(actual, expected)

    # 10 11 12       right None
    expected = pd.DatetimeIndex(
        [
            "2021-01-05 02:00:00+00:00",
            "2021-01-05 03:00:00+00:00",
            "2021-01-05 04:00:00+00:00",
        ],
        tz=tz,
    )
    actual = mcal.date_range(schedule, "1h", closed="right", force_close=None)
    assert_index_equal(actual, expected)

    # 9 10 11 12     both None/ None None
    expected = pd.DatetimeIndex(
        [
            "2021-01-05 01:00:00+00:00",
            "2021-01-05 02:00:00+00:00",
            "2021-01-05 03:00:00+00:00",
            "2021-01-05 04:00:00+00:00",
        ],
        tz=tz,
    )
    actual = mcal.date_range(schedule, "1h", closed="both", force_close=None)
    assert_index_equal(actual, expected)
    actual = mcal.date_range(schedule, "1h", closed=None, force_close=None)
    assert_index_equal(actual, expected)


def test_date_range_daily():
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))

    # If closed='right' and force_close False for daily then the result is empty
    expected = pd.DatetimeIndex([], tz="UTC")
    schedule = cal.schedule("2015-12-31", "2016-01-06")
    with pytest.warns(UserWarning):
        actual = mcal.date_range(schedule, "1D", force_close=False, closed="right")

    assert_index_equal(actual, expected)

    # New years is holiday
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2015-12-31 12:00",
                "2016-01-04 12:00",
                "2016-01-05 12:00",
                "2016-01-06 12:00",
            ]
        ]
    )
    schedule = cal.schedule("2015-12-31", "2016-01-06")
    actual = mcal.date_range(schedule, "1D")

    assert_index_equal(actual, expected)

    # July 3 is early close
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in ["2012-07-02 12:00", "2012-07-03 11:30", "2012-07-04 12:00"]
        ]
    )
    schedule = cal.schedule("2012-07-02", "2012-07-04")
    actual = mcal.date_range(schedule, "1D")

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in ["2016-12-13 12:00", "2016-12-14 11:40", "2016-12-15 12:00"]
        ]
    )
    schedule = cal.schedule("2016-12-13", "2016-12-15")
    actual = mcal.date_range(schedule, "1D")

    assert_index_equal(actual, expected)

    # July 3 is late open
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in ["2012-07-02 09:00", "2012-07-03 11:15", "2012-07-04 09:00"]
        ]
    )
    schedule = cal.schedule("2012-07-02", "2012-07-04")
    actual = mcal.date_range(schedule, "1D", force_close=False, closed=None)

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2016-12-13 11:20",
                "2016-12-13 12:00",
                "2016-12-14 09:00",
                "2016-12-14 11:40",
                "2016-12-15 09:00",
                "2016-12-15 12:00",
            ]
        ]
    )
    schedule = cal.schedule("2016-12-13", "2016-12-15")
    actual = mcal.date_range(schedule, "1D", force_close=True, closed=None)

    assert_index_equal(actual, expected)

    # closed == "left" and force_close= True, should return the same thing
    actual = mcal.date_range(schedule, "1D", force_close=True, closed="left")
    assert_index_equal(actual, expected)


def test_date_range_lower_freq():
    cal = mcal.get_calendar("NYSE")
    schedule = cal.schedule(
        pd.Timestamp("2017-09-05 20:00", tz="UTC"),
        pd.Timestamp("2017-10-23 20:00", tz="UTC"),
    )

    # cannot get date range of frequency lower than 1D
    with pytest.raises(ValueError) as e:
        mcal.date_range(schedule, frequency="3D")
    assert (
        e.exconly()
        == "ValueError: Market Calendar Date_Range Frequency Cannot Be longer than '1D'."
    )

    # instead get for 1D and convert to lower frequency
    short = mcal.date_range(schedule, frequency="1D")
    actual = mcal.convert_freq(short, "3D")
    expected = pd.date_range(
        "2017-09-05 20:00", "2017-10-23 20:00", freq="3D", tz="UTC"
    )
    assert_index_equal(actual, expected)

    actual = mcal.convert_freq(short, "1W")
    expected = pd.date_range(
        "2017-09-05 20:00", "2017-10-23 20:00", freq="1W", tz="UTC"
    )
    assert_index_equal(actual, expected)


def test_date_range_hour():
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(10, 30))

    # New Years Eve and weekend skipped
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2015-12-31 10:00",
                "2015-12-31 10:30",
                "2016-01-04 10:00",
                "2016-01-04 10:30",
                "2016-01-05 10:00",
                "2016-01-05 10:30",
                "2016-01-06 10:00",
                "2016-01-06 10:30",
            ]
        ]
    )
    schedule = cal.schedule("2015-12-31", "2016-01-06")
    actual = mcal.date_range(schedule, "1h", force_close=True)

    assert_index_equal(actual, expected)

    # If force_close False for then result is missing close if not on even increment
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2015-12-31 10:00",
                "2016-01-04 10:00",
                "2016-01-05 10:00",
                "2016-01-06 10:00",
            ]
        ]
    )
    schedule = cal.schedule("2015-12-31", "2016-01-06")
    actual = mcal.date_range(schedule, "1h", force_close=False)

    assert_index_equal(actual, expected)

    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    # July 3 is late open and early close
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2012-07-02 10:00",
                "2012-07-02 11:00",
                "2012-07-02 12:00",
                "2012-07-03 11:30",
                "2012-07-04 10:00",
                "2012-07-04 11:00",
                "2012-07-04 12:00",
            ]
        ]
    )
    schedule = cal.schedule("2012-07-02", "2012-07-04")
    actual = mcal.date_range(schedule, "1h")

    assert_index_equal(actual, expected)

    # Dec 14, 2016 is adhoc early close
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2016-12-14 10:00",
                "2016-12-14 11:00",
                "2016-12-14 11:40",
                "2016-12-15 10:00",
                "2016-12-15 11:00",
                "2016-12-15 12:00",
            ]
        ]
    )
    schedule = cal.schedule("2016-12-14", "2016-12-15")
    actual = mcal.date_range(schedule, "1h")

    assert_index_equal(actual, expected)

    # Dec 13, 2016 is adhoc late open, include the open with closed=True
    expected = pd.DatetimeIndex(
        [
            pd.Timestamp(x, tz=cal.tz).tz_convert("UTC")
            for x in [
                "2016-12-13 11:20",
                "2016-12-13 12:00",
                "2016-12-14 09:00",
                "2016-12-14 10:00",
                "2016-12-14 11:00",
                "2016-12-14 11:40",
            ]
        ]
    )
    schedule = cal.schedule("2016-12-13", "2016-12-14")
    actual = mcal.date_range(schedule, "1h", closed=None)

    assert_index_equal(actual, expected)


def test_date_range_minute():
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(10, 30))

    # New Years Eve and weekend skipped
    schedule = cal.schedule("2015-12-31", "2016-01-06")
    actual = mcal.date_range(schedule, "1min", force_close=True)
    assert len(actual) == 4 * 90
    assert actual[0] == pd.Timestamp("2015-12-31 09:01", tz=cal.tz)
    assert actual[len(actual) - 1] == pd.Timestamp("2016-01-06 10:30", tz=cal.tz)

    for x in [
        "2015-12-31 09:02",
        "2015-12-31 10:30",
        "2016-01-04 09:01",
        "2016-01-06 09:01",
    ]:
        assert pd.Timestamp(x, tz=cal.tz) in actual

    for x in [
        "2015-12-31 09:00",
        "2015-12-31 10:31",
        "2016-01-02 09:01",
        "2016-01-03 09:01",
        "2016-01-06 09:00",
    ]:
        assert pd.Timestamp(x, tz=cal.tz) not in actual

    # July 3 is late open and early close
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    schedule = cal.schedule("2012-07-02", "2012-07-04")
    actual = mcal.date_range(schedule, "1min")
    assert len(actual) == 375  # 2 days of 3 hours, and one day of 15 mins
    assert actual[0] == pd.Timestamp("2012-07-02 09:01", tz=cal.tz)
    assert actual[len(actual) - 1] == pd.Timestamp("2012-07-04 12:00", tz=cal.tz)

    for x in [
        "2012-07-02 09:02",
        "2012-07-02 12:00",
        "2012-07-03 11:16",
        "2012-07-03 11:30",
        "2012-07-04 09:01",
    ]:
        assert pd.Timestamp(x, tz=cal.tz) in actual

    for x in [
        "2012-07-02 09:00",
        "2012-07-02 12:01",
        "2012-07-03 11:15",
        "2012-07-03 11:31",
        "2012-07-04 09:00",
    ]:
        assert pd.Timestamp(x, tz=cal.tz) not in actual

    # Dec 13, 2016 is ad-hoc late open, include the open with closed=True, Dec 14 is ad-hoc early close
    cal = FakeCalendar(open_time=datetime.time(9, 0), close_time=datetime.time(12, 0))
    schedule = cal.schedule("2016-12-13", "2016-12-14")
    actual = mcal.date_range(schedule, "1min", closed=None)

    assert len(actual) == 41 + (61 + 60 + 40)
    assert actual[0] == pd.Timestamp("2016-12-13 11:20", tz=cal.tz)
    assert actual[len(actual) - 1] == pd.Timestamp("2016-12-14 11:40", tz=cal.tz)

    for x in ["2016-12-13 11:21", "2016-12-13 12:00", "2016-12-14 09:00"]:
        assert pd.Timestamp(x, tz=cal.tz) in actual

    for x in [
        "2016-12-13 11:19",
        "2016-12-13 12:01",
        "2016-12-14 08:59",
        "2016-12-14 11:41",
    ]:
        assert pd.Timestamp(x, tz=cal.tz) not in actual


def test_date_range_w_breaks():
    cal = FakeBreakCalendar()
    schedule = cal.schedule("2016-12-28", "2016-12-28")

    with pytest.warns(UserWarning):
        mcal.date_range(schedule, "1h", closed="right", force_close=False)

    expected = [
        "2016-12-28 14:30:00+00:00",
        "2016-12-28 15:00:00+00:00",
        "2016-12-28 16:00:00+00:00",
        "2016-12-28 16:30:00+00:00",
        "2016-12-28 17:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "30min", closed=None)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = [
        "2016-12-28 15:00:00+00:00",
        "2016-12-28 16:30:00+00:00",
        "2016-12-28 17:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "30min", closed="right")
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = [
        "2016-12-28 14:30:00+00:00",
        "2016-12-28 16:00:00+00:00",
        "2016-12-28 16:30:00+00:00",
    ]
    actual = mcal.date_range(schedule, "30min", closed="left", force_close=False)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = [
        "2016-12-28 14:30:00+00:00",
        "2016-12-28 15:00:00+00:00",
        "2016-12-28 16:00:00+00:00",
        "2016-12-28 16:30:00+00:00",
        "2016-12-28 17:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "30min", closed="left", force_close=True)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    # when the open is the break start
    schedule = cal.schedule("2016-12-29", "2016-12-29")
    expected = [
        "2016-12-29 16:00:00+00:00",
        "2016-12-29 16:15:00+00:00",
        "2016-12-29 16:30:00+00:00",
        "2016-12-29 16:45:00+00:00",
        "2016-12-29 17:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "15min", closed=None)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = [
        "2016-12-29 16:15:00+00:00",
        "2016-12-29 16:30:00+00:00",
        "2016-12-29 16:45:00+00:00",
        "2016-12-29 17:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "15min", closed="right")
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    # when the close is the break end
    schedule = cal.schedule("2016-12-30", "2016-12-30")

    # force close True
    expected = [
        "2016-12-30 14:30:00+00:00",
        "2016-12-30 14:45:00+00:00",
        "2016-12-30 15:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "15min", closed=None, force_close=True)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    # force close False
    expected = [
        "2016-12-30 14:30:00+00:00",
        "2016-12-30 14:45:00+00:00",
        "2016-12-30 15:00:00+00:00",
    ]
    actual = mcal.date_range(schedule, "15min", closed=None, force_close=False)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual

    expected = ["2016-12-30 14:45:00+00:00", "2016-12-30 15:00:00+00:00"]
    actual = mcal.date_range(schedule, "15min", closed="right", force_close=False)
    assert len(actual) == len(expected)
    for x in expected:
        assert pd.Timestamp(x) in actual


@pytest.mark.parametrize("merge", [True, False])
def test_session_list_gen(merge: bool):

    schedule = pd.DataFrame(
        [
            {
                "pre": pd.Timestamp("2021-01-05T7:00"),
                "market_open": pd.Timestamp("2021-01-05T9:00"),
                "break_start": pd.Timestamp("2021-01-05T1:30"),
                "break_end": pd.Timestamp("2021-01-05T2:00"),
                "market_close": pd.Timestamp("2021-01-05T3:00"),
                "post": pd.Timestamp("2021-01-05T7:00"),
            }
        ],
        index=[pd.Timestamp("2021-01-05")],
    )
    cols = set(schedule.columns)

    # region ---- ---- Regular Trading Hours w/ Breaks ---- ----
    # Leaves breaks when they are in schedule
    assert _make_session_list(cols, "RTH", merge)[0] == [
        ("market_open", "break_start"),
        ("break_end", "market_close"),
    ]
    assert _make_session_list(cols, ["pre_break", "post_break"], merge)[0] == [
        ("market_open", "break_start"),
        ("break_end", "market_close"),
    ]
    assert _make_session_list(cols, ["pre_break"], merge)[0] == [
        ("market_open", "break_start"),
    ]
    assert _make_session_list(cols, ["post_break"], merge)[0] == [
        ("break_end", "market_close"),
    ]

    # ignores breaks when they aren't in the schedule
    assert _make_session_list(cols - {"break_start", "break_end"}, "RTH", merge)[0] == [
        ("market_open", "market_close"),
    ]
    # endregion

    # region ---- ---- Extended Trading Hours ---- ----
    assert _make_session_list(cols, "ETH", merge)[0] == [
        ("pre", "market_open"),
        ("market_close", "post"),
    ]
    assert _make_session_list(cols, ["pre", "post"], merge)[0] == [
        ("pre", "market_open"),
        ("market_close", "post"),
    ]

    # Drop 'pre' / 'post' individually when those aren't present
    with pytest.warns(MissingSessionWarning) as w4:
        assert _make_session_list(cols - {"pre"}, "ETH", merge)[0] == [
            ("market_close", "post"),
        ]
    with pytest.warns(MissingSessionWarning) as w5:
        assert _make_session_list(cols - {"post"}, "ETH", merge)[0] == [
            ("pre", "market_open"),
        ]
    assert w4 and w5
    # endregion

    # region ---- ---- Closed Hours ---- ----
    assert _make_session_list(cols, "closed", merge) == (
        [
            ("post", "pre_wrap"),
        ],
        False,
    )
    assert _make_session_list(cols - {"post", "pre"}, "closed", merge) == (
        [
            ("market_close", "market_open_wrap"),
        ],
        False,
    )
    assert _make_session_list(cols, "closed_masked", merge) == (
        [
            ("post", "pre_wrap"),
        ],
        True,
    )
    assert _make_session_list(cols - {"post", "pre"}, "closed_masked", merge) == (
        [
            ("market_close", "market_open_wrap"),
        ],
        True,
    )
    # endregion

    # region ---- ---- Error and Warnings on Missing sessions ---- ----
    # escalate missing sessions to errors
    filter_date_range_warnings("error", MissingSessionWarning)
    with pytest.raises(MissingSessionWarning) as e1:
        _ = _make_session_list(cols - {"market_open"}, ["RTH", "pre"], merge)
    # Commented direct check out since the actual order of the missing values can change
    # since sets are not ordered. plus, this tests the 'missing' functions
    # assert e1.exconly() == (
    #     "pandas_market_calendars.calendar_utils.MissingSessionWarning: Requested Sessions: "
    #     "['pre', 'pre_break'], but schedule is missing columns: ['market_open']."
    #     "\nResulting DatetimeIndex will lack those sessions."
    # )
    assert missing_columns(e1.value) == {"market_open"}
    assert missing_sessions(e1.value) == {"pre", "pre_break"}

    with pytest.raises(MissingSessionWarning) as e2:
        _ = _make_session_list(cols - {"market_close"}, "RTH", merge)
    assert missing_columns(e2.value) == {"market_close"}
    assert missing_sessions(e2.value) == {"post_break"}

    with pytest.raises(MissingSessionWarning) as e3:
        _ = _make_session_list(cols - {"market_open", "market_close"}, "RTH", merge)
    assert missing_columns(e3.value) == {"market_close", "market_open"}
    assert missing_sessions(e3.value) == {"post_break", "pre_break"}

    # Deescalate errors and check warnings are thrown
    filter_date_range_warnings("default", MissingSessionWarning)
    with pytest.warns(MissingSessionWarning) as w1:
        _ = _make_session_list(cols - {"market_open"}, ["RTH", "pre"], merge)
    with pytest.warns(MissingSessionWarning) as w2:
        _ = _make_session_list(cols - {"market_close"}, "RTH", merge)
    with pytest.warns(MissingSessionWarning) as w3:
        _ = _make_session_list(cols - {"market_open", "market_close"}, "RTH", merge)
    assert all((w1, w2, w3))
    # endregion


def test_session_list_merge_adj():
    schedule = pd.DataFrame(
        [
            {
                "pre": pd.Timestamp("2021-01-05T7:00"),
                "market_open": pd.Timestamp("2021-01-05T9:00"),
                "break_start": pd.Timestamp("2021-01-05T1:30"),
                "break_end": pd.Timestamp("2021-01-05T2:00"),
                "market_close": pd.Timestamp("2021-01-05T3:00"),
                "post": pd.Timestamp("2021-01-05T7:00"),
            }
        ],
        index=[pd.Timestamp("2021-01-05")],
    )
    cols = set(schedule.columns)

    # ETH Post sessions merge/split
    assert _make_session_list(cols - {"pre"}, ["closed", "post_break"], True)[0] == [
        ("break_end", "market_close"),
        ("post", "market_open_wrap"),
    ]
    assert _make_session_list(cols - {"post", "pre"}, ["closed", "post_break"], True)[
        0
    ] == [
        ("break_end", "market_open_wrap"),
    ]

    # Break Merge/Split
    assert _make_session_list(cols, ["RTH"], True)[0] == [
        ("market_open", "break_start"),
        ("break_end", "market_close"),
    ]
    assert _make_session_list(cols, ["RTH", "break"], True)[0] == [
        ("market_open", "market_close"),
    ]

    # 'ETH' & 'RTH' Merge /split
    assert _make_session_list(cols, ["RTH", "ETH"], True)[0] == [
        ("pre", "break_start"),
        ("break_end", "post"),
    ]
    assert _make_session_list(
        cols - {"break_start", "break_end"}, ["RTH", "ETH"], True
    )[0] == [
        ("pre", "post"),
    ]

    # all sessions: pd.daterange equivalent
    assert _make_session_list(cols, ["RTH", "ETH", "break", "closed"], True)[0] == [
        ("pre", "pre_wrap"),
    ]
    assert _make_session_list(cols - {"pre", "post"}, ["RTH", "break", "closed"], True)[
        0
    ] == [
        ("market_open", "market_open_wrap"),
    ]
