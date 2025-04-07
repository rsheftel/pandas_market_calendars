import datetime

import pandas as pd
import pytest
from pandas.testing import assert_index_equal

import pandas_market_calendars as mcal
from tests.test_market_calendar import FakeCalendar, FakeBreakCalendar, FakeETHCalendar

from pandas_market_calendars.calendar_utils import (
    InsufficientScheduleWarning,
    MissingSessionWarning,
    _make_session_list,
    DisappearingSessionWarning,
    OverlappingSessionWarning,
    date_range_htf,
    filter_date_range_warnings,
    parse_missing_session_warning,
    parse_insufficient_schedule_warning,
)

# region ---- ---- ---- Date Range LTF ---- ---- ----


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
    filter_date_range_warnings("error", [OverlappingSessionWarning, InsufficientScheduleWarning])

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
            e.exconly() == "pandas_market_calendars.calendar_utils.OverlappingSessionWarning: "
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

    filter_date_range_warnings("error", InsufficientScheduleWarning)

    # Insuffient Schedule. (start/end times exceed values in the schedule)
    with pytest.raises(InsufficientScheduleWarning) as e4:
        mcal.date_range(bschedule, "2h", start="2021-01-03", end="2021-01-05")
    assert parse_insufficient_schedule_warning(e4.value) == (
        True,
        pd.Timestamp("2021-01-03"),
        pd.Timestamp("2021-01-04"),
    )

    with pytest.raises(InsufficientScheduleWarning) as e5:
        mcal.date_range(bschedule, "2h", start="2021-01-05", end="2021-01-07")
    assert parse_insufficient_schedule_warning(e5.value) == (
        False,
        pd.Timestamp("2021-01-06"),
        pd.Timestamp("2021-01-06"),
    )

    filter_date_range_warnings("default", OverlappingSessionWarning)
    # Insuffient Schedule again, but as a warning
    with pytest.warns(InsufficientScheduleWarning) as w4:
        mcal.date_range(bschedule, "2h", start="2021-01-03", end="2021-01-05")

    with pytest.warns(InsufficientScheduleWarning) as w5:
        mcal.date_range(bschedule, "2h", start="2021-01-05", end="2021-01-07")

    assert all([w4, w5])

    with pytest.raises(ValueError) as e3:
        mcal.date_range(bschedule, "2h", start="2021-01-06", end="2021-01-03")
    # should't raise a value error
    mcal.date_range(bschedule, "2h", start="2021-01-05", end="2021-01-05")

    try:
        # should all be fine, since force_close cuts the overlapping interval
        mcal.date_range(bschedule, "2h", closed="right", force_close=True)

        with pytest.warns(DisappearingSessionWarning):  # should also warn about lost sessions
            mcal.date_range(bschedule, "2h", closed="right", force_close=False)

        mcal.date_range(bschedule, "2h", closed="both", force_close=True)
        mcal.date_range(bschedule, "2h", closed="both", force_close=False)
        # closed = "left" should never be a problem since it won't go outside market hours anyway
        mcal.date_range(bschedule, "2h", closed="left", force_close=True)
        mcal.date_range(bschedule, "2h", closed="left", force_close=False)
        mcal.date_range(bschedule, "2h", closed="left", force_close=None)
    except ValueError as e:
        pytest.fail(f"Unexpected Error: \n{e}")


@pytest.mark.parametrize("merge", [True, False])
def test_session_list_gen(merge: bool):
    # Only Generating Session Lists to test a sub component of date_range to ease de-bugging
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
    assert parse_missing_session_warning(e1.value) == (
        {"pre", "pre_break"},
        {"market_open"},
    )

    with pytest.raises(MissingSessionWarning) as e2:
        _ = _make_session_list(cols - {"market_close"}, "RTH", merge)
    assert parse_missing_session_warning(e2.value) == ({"post_break"}, {"market_close"})

    with pytest.raises(MissingSessionWarning) as e3:
        _ = _make_session_list(cols - {"market_open", "market_close"}, "RTH", merge)
    assert parse_missing_session_warning(e3.value) == (
        {"post_break", "pre_break"},
        {"market_close", "market_open"},
    )

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
    # Only Generating Session Lists and Making sure adjacent sessions merge
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
    assert _make_session_list(cols - {"post", "pre"}, ["closed", "post_break"], True)[0] == [
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
    assert _make_session_list(cols - {"break_start", "break_end"}, ["RTH", "ETH"], True)[0] == [
        ("pre", "post"),
    ]

    # all sessions: pd.daterange equivalent
    assert _make_session_list(cols, ["RTH", "ETH", "break", "closed"], True)[0] == [
        ("pre", "pre_wrap"),
    ]
    assert _make_session_list(cols - {"pre", "post"}, ["RTH", "break", "closed"], True)[0] == [
        ("market_open", "market_open_wrap"),
    ]


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
    expected = pd.DatetimeIndex(["2021-01-05 02:00:00+00:00", "2021-01-05 03:00:00+00:00"], tz=tz)
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
    assert e.exconly() == "ValueError: Market Calendar Date_Range Frequency Cannot Be longer than '1D'."

    # instead get for 1D and convert to lower frequency
    short = mcal.date_range(schedule, frequency="1D")
    actual = mcal.convert_freq(short, "3D")
    expected = pd.date_range("2017-09-05 20:00", "2017-10-23 20:00", freq="3D", tz="UTC")
    assert_index_equal(actual, expected)

    actual = mcal.convert_freq(short, "1W")
    expected = pd.date_range("2017-09-05 20:00", "2017-10-23 20:00", freq="1W", tz="UTC")
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


@pytest.mark.parametrize("tz", ["America/New_York", "Asia/Ulaanbaatar", "UTC"])
def test_date_range_ETH(tz):

    cal = FakeETHCalendar()
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=tz)

    # Merges Sessions, Keeps all timestamps at Hour mark
    assert_index_equal(
        mcal.date_range(schedule, "1h", "left", False, {"RTH", "ETH"}),
        pd.DatetimeIndex(
            [
                "2016-12-30 08:00:00-05:00",
                "2016-12-30 09:00:00-05:00",
                "2016-12-30 10:00:00-05:00",
                "2016-12-30 11:00:00-05:00",
                "2016-12-30 12:00:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 09:00:00-05:00",
                "2017-01-03 10:00:00-05:00",
                "2017-01-03 11:00:00-05:00",
                "2017-01-03 12:00:00-05:00",
            ],
            tz=tz,
        ),
    )

    # Splits Sessions, Adjusts timestamps to align with sessions
    assert_index_equal(
        mcal.date_range(schedule, 3600, "left", False, {"RTH", "ETH"}, False),
        pd.DatetimeIndex(
            [
                "2016-12-30 08:00:00-05:00",
                "2016-12-30 09:00:00-05:00",
                "2016-12-30 09:30:00-05:00",
                "2016-12-30 10:30:00-05:00",
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 12:30:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 09:00:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 10:30:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 12:30:00-05:00",
            ],
            tz=tz,
        ),
    )

    # ETH Hours only
    assert_index_equal(
        mcal.date_range(schedule, 3600, "left", False, "ETH", False),
        pd.DatetimeIndex(
            [
                "2016-12-30 08:00:00-05:00",
                "2016-12-30 09:00:00-05:00",
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 12:30:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 09:00:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 12:30:00-05:00",
            ],
            tz=tz,
        ),
    )

    # Pre Hours only
    assert_index_equal(
        mcal.date_range(schedule, pd.Timedelta("1h"), "left", False, "pre"),
        pd.DatetimeIndex(
            [
                "2016-12-30 08:00:00-05:00",
                "2016-12-30 09:00:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 09:00:00-05:00",
            ],
            tz=tz,
        ),
    )

    # Post Hours only
    assert_index_equal(
        mcal.date_range(schedule, pd.Timedelta("1h"), "left", False, "post"),
        pd.DatetimeIndex(
            [
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 12:30:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 12:30:00-05:00",
            ],
            tz=tz,
        ),
    )


@pytest.mark.parametrize("tz", ["America/New_York", "Asia/Ulaanbaatar", "UTC"])
def test_date_range_start_end(tz):
    cal = FakeETHCalendar()
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=tz)

    # Trim the Start to the desired timestamp
    actual1 = pd.DatetimeIndex(
        [
            "2016-12-30 10:00:00-05:00",
            "2016-12-30 10:30:00-05:00",
            "2016-12-30 11:00:00-05:00",
            "2016-12-30 11:30:00-05:00",
            "2017-01-03 09:30:00-05:00",
            "2017-01-03 10:00:00-05:00",
            "2017-01-03 10:30:00-05:00",
            "2017-01-03 11:00:00-05:00",
            "2017-01-03 11:30:00-05:00",
        ],
        tz=tz,
    )

    # trims off the 9:30 Timestamp
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-30T10:00-5:00"),
        actual1,
    )
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-30T9:59-5:00"),
        actual1,
    )
    # trims off the 10am timestamp too
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-30T10:01-5:00"),
        actual1[1 : len(actual1)],
    )
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-30T10:00-5:00", periods=3),
        actual1[0:-6],
    )

    # Check both start and end work in conjunction and periods are ignored
    assert_index_equal(
        mcal.date_range(
            schedule,
            "30m",
            "left",
            True,
            start="2016-12-30T11:00-5:00",
            end="2017-01-03 11:00:00-05:00",
            periods=2,
        ),
        actual1[2:-1],
    )

    # Trim the End to the desired timestamp
    actual2 = pd.DatetimeIndex(
        [
            "2016-12-30 09:30:00-05:00",
            "2016-12-30 10:00:00-05:00",
            "2016-12-30 10:30:00-05:00",
            "2016-12-30 11:00:00-05:00",
        ],
        tz=tz,
    )

    # trims off the 11:30 Timestamp
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T11:01-5:00"),
        actual2,
    )
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T11:00-5:00"),
        actual2,
    )
    # trims off the 11am timestamp too
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T10:59-5:00"),
        actual2[0:-1],
    )
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T11:00-5:00", periods=2),
        actual2[2 : len(actual2)],
    )

    # Start / End are interpreted in the Schedule's Timezone
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=cal.tz)
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-30T10:00"),
        actual1.tz_convert(cal.tz),
    )
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T11:00"),
        actual2.tz_convert(cal.tz),
    )


@pytest.mark.parametrize("tz", ["America/New_York", "Asia/Ulaanbaatar", "UTC"])
def test_date_range_catch_periods_err(tz):
    cal = FakeETHCalendar()
    # ---- ---- Attempt to throw an warning, catch it, then recover. ---- ----
    filter_date_range_warnings("error", InsufficientScheduleWarning)

    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=tz)
    with pytest.raises(InsufficientScheduleWarning) as e1:
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-29T10:00")

    # Update the Schedule to what is needed in a recovery attempt
    _bool, t1, t2 = parse_insufficient_schedule_warning(e1.value)
    if _bool:
        schedule = pd.concat([cal.schedule(t1, t2, market_times="all", tz=tz), schedule])
    else:
        assert False

    # Retest with the updated schedule
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2016-12-29T10:00:00-5:00"),
        pd.DatetimeIndex(
            [
                "2016-12-29 10:00:00-05:00",
                "2016-12-29 10:30:00-05:00",
                "2016-12-29 11:00:00-05:00",
                "2016-12-29 11:30:00-05:00",
                "2016-12-30 09:30:00-05:00",
                "2016-12-30 10:00:00-05:00",
                "2016-12-30 10:30:00-05:00",
                "2016-12-30 11:00:00-05:00",
                "2016-12-30 11:30:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 10:00:00-05:00",
                "2017-01-03 10:30:00-05:00",
                "2017-01-03 11:00:00-05:00",
                "2017-01-03 11:30:00-05:00",
            ],
            tz=tz,
        ),
    )

    #  ---- ---- Attempt To Throw and catch an error on End Time ---- ----
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=tz)
    with pytest.raises(InsufficientScheduleWarning) as e1:
        mcal.date_range(schedule, "30m", "left", True, end="2017-01-04T11:00-5:00")

    # Update the Schedule to what is needed in a recovery attempt
    _bool, t1, t2 = parse_insufficient_schedule_warning(e1.value)
    if _bool:
        assert False
    else:
        schedule = pd.concat([schedule, cal.schedule(t1, t2, market_times="all", tz=tz)])

    # Retest with the updated schedule
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2017-01-04T11:00-5:00"),
        pd.DatetimeIndex(
            [
                "2016-12-30 09:30:00-05:00",
                "2016-12-30 10:00:00-05:00",
                "2016-12-30 10:30:00-05:00",
                "2016-12-30 11:00:00-05:00",
                "2016-12-30 11:30:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 10:00:00-05:00",
                "2017-01-03 10:30:00-05:00",
                "2017-01-03 11:00:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-04 09:30:00-05:00",
                "2017-01-04 10:00:00-05:00",
                "2017-01-04 10:30:00-05:00",
                "2017-01-04 11:00:00-05:00",
            ],
            tz=tz,
        ),
    )

    # ---- ---- Attempt To Throw and catch an insufficient # of periods from start ---- ----
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=tz)
    with pytest.raises(InsufficientScheduleWarning) as e1:
        mcal.date_range(schedule, "30m", "left", True, start="2017-01-03T10:00-5:00", periods=8)

    # Update the Schedule to what is needed in a recovery attempt
    _bool, t1, t2 = parse_insufficient_schedule_warning(e1.value)
    if _bool:
        assert False
    else:
        schedule = pd.concat([schedule, cal.schedule(t1, t2, market_times="all", tz=tz)])

    # Retest with the updated schedule
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, start="2017-01-03T10:00-5:00", periods=8),
        pd.DatetimeIndex(
            [
                "2017-01-03 10:00:00-05:00",
                "2017-01-03 10:30:00-05:00",
                "2017-01-03 11:00:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-04 09:30:00-05:00",
                "2017-01-04 10:00:00-05:00",
                "2017-01-04 10:30:00-05:00",
                "2017-01-04 11:00:00-05:00",
            ],
            tz=tz,
        ),
    )

    # ---- ---- Attempt To Throw and catch an insufficient # of periods from end ---- ----
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=tz)
    with pytest.raises(InsufficientScheduleWarning) as e1:
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T11:00-5:00", periods=8)

    # Update the Schedule to what is needed in a recovery attempt
    _bool, t1, t2 = parse_insufficient_schedule_warning(e1.value)
    if _bool:
        schedule = pd.concat([cal.schedule(t1, t2, market_times="all", tz=tz), schedule])
    else:
        assert False

    # Retest with the updated schedule
    assert_index_equal(
        mcal.date_range(schedule, "30m", "left", True, end="2016-12-30T11:00-5:00", periods=8),
        pd.DatetimeIndex(
            [
                "2016-12-29 10:00:00-05:00",
                "2016-12-29 10:30:00-05:00",
                "2016-12-29 11:00:00-05:00",
                "2016-12-29 11:30:00-05:00",
                "2016-12-30 09:30:00-05:00",
                "2016-12-30 10:00:00-05:00",
                "2016-12-30 10:30:00-05:00",
                "2016-12-30 11:00:00-05:00",
            ],
            tz=tz,
        ),
    )

    filter_date_range_warnings("default")


def test_date_range_closed():
    # This section cannot be parameterized because the results are not consitant
    # across TZs. This is the result of the sessions ending at midnight of the
    # TZ of the schedule, not the TZ of the exchange. The TZ of the exchange is
    # not known by date_range and thus the results cannot be made consistent.
    cal = FakeETHCalendar()
    schedule = cal.schedule("2016-12-30", "2017-01-03", market_times="all", tz=cal.tz)

    # Post-to-Pre Keeping all The Time closed
    assert_index_equal(
        mcal.date_range(schedule, "4h", "left", None, "closed"),
        pd.DatetimeIndex(
            [
                "2016-12-30 13:00:00-05:00",
                "2016-12-30 17:00:00-05:00",
                "2016-12-30 21:00:00-05:00",
                "2016-12-31 01:00:00-05:00",
                "2016-12-31 05:00:00-05:00",
                "2016-12-31 09:00:00-05:00",
                "2016-12-31 13:00:00-05:00",
                "2016-12-31 17:00:00-05:00",
                "2016-12-31 21:00:00-05:00",
                "2017-01-01 01:00:00-05:00",
                "2017-01-01 05:00:00-05:00",
                "2017-01-01 09:00:00-05:00",
                "2017-01-01 13:00:00-05:00",
                "2017-01-01 17:00:00-05:00",
                "2017-01-01 21:00:00-05:00",
                "2017-01-02 01:00:00-05:00",
                "2017-01-02 05:00:00-05:00",
                "2017-01-02 09:00:00-05:00",
                "2017-01-02 13:00:00-05:00",
                "2017-01-02 17:00:00-05:00",
                "2017-01-02 21:00:00-05:00",
                "2017-01-03 01:00:00-05:00",
                "2017-01-03 05:00:00-05:00",
                "2017-01-03 13:00:00-05:00",
                "2017-01-03 17:00:00-05:00",
                "2017-01-03 21:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    # Post to Pre Dropping Holiday and weekends
    assert_index_equal(
        mcal.date_range(schedule, "4h", "left", False, "closed_masked", False),
        pd.DatetimeIndex(
            [
                "2016-12-30 13:00:00-05:00",
                "2016-12-30 17:00:00-05:00",
                "2016-12-30 21:00:00-05:00",
                "2017-01-03 00:00:00-05:00",
                "2017-01-03 04:00:00-05:00",
                "2017-01-03 13:00:00-05:00",
                "2017-01-03 17:00:00-05:00",
                "2017-01-03 21:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    # Same But market_close to pre

    assert_index_equal(
        mcal.date_range(schedule.drop(columns=["post"]), "4h", "both", session="closed"),
        pd.DatetimeIndex(
            [
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 15:30:00-05:00",
                "2016-12-30 19:30:00-05:00",
                "2016-12-30 23:30:00-05:00",
                "2016-12-31 03:30:00-05:00",
                "2016-12-31 07:30:00-05:00",
                "2016-12-31 11:30:00-05:00",
                "2016-12-31 15:30:00-05:00",
                "2016-12-31 19:30:00-05:00",
                "2016-12-31 23:30:00-05:00",
                "2017-01-01 03:30:00-05:00",
                "2017-01-01 07:30:00-05:00",
                "2017-01-01 11:30:00-05:00",
                "2017-01-01 15:30:00-05:00",
                "2017-01-01 19:30:00-05:00",
                "2017-01-01 23:30:00-05:00",
                "2017-01-02 03:30:00-05:00",
                "2017-01-02 07:30:00-05:00",
                "2017-01-02 11:30:00-05:00",
                "2017-01-02 15:30:00-05:00",
                "2017-01-02 19:30:00-05:00",
                "2017-01-02 23:30:00-05:00",
                "2017-01-03 03:30:00-05:00",
                "2017-01-03 07:30:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 15:30:00-05:00",
                "2017-01-03 19:30:00-05:00",
                "2017-01-03 23:30:00-05:00",
                "2017-01-04 00:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    assert_index_equal(
        mcal.date_range(schedule.drop(columns=["post"]), "4h", "both", session="closed_masked"),
        pd.DatetimeIndex(
            [
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 15:30:00-05:00",
                "2016-12-30 19:30:00-05:00",
                "2016-12-30 23:30:00-05:00",
                "2016-12-31 00:00:00-05:00",
                "2017-01-03 00:00:00-05:00",
                "2017-01-03 04:00:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 15:30:00-05:00",
                "2017-01-03 19:30:00-05:00",
                "2017-01-03 23:30:00-05:00",
                "2017-01-04 00:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    # Again But post to market_open

    assert_index_equal(
        mcal.date_range(schedule.drop(columns=["pre"]), "4h", "both", session="closed"),
        pd.DatetimeIndex(
            [
                "2016-12-30 13:00:00-05:00",
                "2016-12-30 17:00:00-05:00",
                "2016-12-30 21:00:00-05:00",
                "2016-12-31 01:00:00-05:00",
                "2016-12-31 05:00:00-05:00",
                "2016-12-31 09:00:00-05:00",
                "2016-12-31 13:00:00-05:00",
                "2016-12-31 17:00:00-05:00",
                "2016-12-31 21:00:00-05:00",
                "2017-01-01 01:00:00-05:00",
                "2017-01-01 05:00:00-05:00",
                "2017-01-01 09:00:00-05:00",
                "2017-01-01 13:00:00-05:00",
                "2017-01-01 17:00:00-05:00",
                "2017-01-01 21:00:00-05:00",
                "2017-01-02 01:00:00-05:00",
                "2017-01-02 05:00:00-05:00",
                "2017-01-02 09:00:00-05:00",
                "2017-01-02 13:00:00-05:00",
                "2017-01-02 17:00:00-05:00",
                "2017-01-02 21:00:00-05:00",
                "2017-01-03 01:00:00-05:00",
                "2017-01-03 05:00:00-05:00",
                "2017-01-03 09:00:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 13:00:00-05:00",
                "2017-01-03 17:00:00-05:00",
                "2017-01-03 21:00:00-05:00",
                "2017-01-04 00:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    assert_index_equal(
        mcal.date_range(schedule.drop(columns=["pre"]), "4h", "both", session="closed_masked"),
        pd.DatetimeIndex(
            [
                "2016-12-30 13:00:00-05:00",
                "2016-12-30 17:00:00-05:00",
                "2016-12-30 21:00:00-05:00",
                "2016-12-31 00:00:00-05:00",
                "2017-01-03 00:00:00-05:00",
                "2017-01-03 04:00:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 13:00:00-05:00",
                "2017-01-03 17:00:00-05:00",
                "2017-01-03 21:00:00-05:00",
                "2017-01-04 00:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    # Again But market_close to market_open

    assert_index_equal(
        mcal.date_range(schedule.drop(columns=["pre", "post"]), "4h", "both", session="closed"),
        pd.DatetimeIndex(
            [
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 15:30:00-05:00",
                "2016-12-30 19:30:00-05:00",
                "2016-12-30 23:30:00-05:00",
                "2016-12-31 03:30:00-05:00",
                "2016-12-31 07:30:00-05:00",
                "2016-12-31 11:30:00-05:00",
                "2016-12-31 15:30:00-05:00",
                "2016-12-31 19:30:00-05:00",
                "2016-12-31 23:30:00-05:00",
                "2017-01-01 03:30:00-05:00",
                "2017-01-01 07:30:00-05:00",
                "2017-01-01 11:30:00-05:00",
                "2017-01-01 15:30:00-05:00",
                "2017-01-01 19:30:00-05:00",
                "2017-01-01 23:30:00-05:00",
                "2017-01-02 03:30:00-05:00",
                "2017-01-02 07:30:00-05:00",
                "2017-01-02 11:30:00-05:00",
                "2017-01-02 15:30:00-05:00",
                "2017-01-02 19:30:00-05:00",
                "2017-01-02 23:30:00-05:00",
                "2017-01-03 03:30:00-05:00",
                "2017-01-03 07:30:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 15:30:00-05:00",
                "2017-01-03 19:30:00-05:00",
                "2017-01-03 23:30:00-05:00",
                "2017-01-04 00:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )

    assert_index_equal(
        mcal.date_range(
            schedule.drop(columns=["pre", "post"]),
            "4h",
            "both",
            session="closed_masked",
        ),
        pd.DatetimeIndex(
            [
                "2016-12-30 11:30:00-05:00",
                "2016-12-30 15:30:00-05:00",
                "2016-12-30 19:30:00-05:00",
                "2016-12-30 23:30:00-05:00",
                "2016-12-31 00:00:00-05:00",
                "2017-01-03 00:00:00-05:00",
                "2017-01-03 04:00:00-05:00",
                "2017-01-03 08:00:00-05:00",
                "2017-01-03 09:30:00-05:00",
                "2017-01-03 11:30:00-05:00",
                "2017-01-03 15:30:00-05:00",
                "2017-01-03 19:30:00-05:00",
                "2017-01-03 23:30:00-05:00",
                "2017-01-04 00:00:00-05:00",
            ],
            tz=cal.tz,
        ),
    )


# endregion

# region ---- ---- ---- Date Range HTF ---- ---- ----


def test_date_range_htf_exceptions():
    cal = FakeCalendar().holidays()

    with pytest.raises(ValueError):
        date_range_htf(cal, "1D", "2020-01-01", "2025-01-01", "left")
    with pytest.raises(ValueError):
        date_range_htf(cal, "1D", "2020-01-01", 1e9)
    with pytest.raises(ValueError):
        date_range_htf(cal, "1D", "2025-01-01", "2020-01-01")
    with pytest.raises(ValueError):
        date_range_htf(cal, "1h", "2020-01-01", "2025-01-01")
    with pytest.raises(ValueError):
        date_range_htf(cal, "1.6D", "2020-01-01", "2025-01-01")
    with pytest.raises(ValueError):
        date_range_htf(cal, "1D", "2020-01-01")
    with pytest.raises(ValueError):
        date_range_htf(cal, "-1D", "2020-01-01", "2025-01-01")
    with pytest.raises(ValueError):
        date_range_htf(cal, "1D", "2020-01-01", None, -10)
    with pytest.raises(ValueError):
        date_range_htf(cal, "", "2020-01-01", None, 10)

    assert len(date_range_htf(cal, "1W", "2020-01-01", None, 10)) == 10
    assert len(date_range_htf(cal, "2W", "2020-01-01", None, 10)) == 10
    assert len(date_range_htf(cal, "2M", "2020-01-01", None, 10)) == 10
    assert len(date_range_htf(cal, "4Q", "2020-01-01", None, 10)) == 10
    assert len(date_range_htf(cal, "2Y", "2020-01-01", None, 10)) == 10


def test_date_range_htf_days():
    cal = FakeCalendar().holidays()
    reference = pd.date_range("2020-01-01", "2021-01-01", freq=cal)

    assert_index_equal(reference, date_range_htf(cal, "1D", "2020-01-01", "2021-01-01"))

    assert_index_equal(reference[::2], date_range_htf(cal, "2D", "2020-01-01", "2021-01-01"))
    assert_index_equal(reference[::5], date_range_htf(cal, "5D", "2020-01-01", "2021-01-01"))
    assert_index_equal(reference[:20], date_range_htf(cal, "1D", "2020-01-01", None, 20))
    assert_index_equal(reference[-20:], date_range_htf(cal, "1D", None, "2021-01-01", 20))
    assert_index_equal(pd.DatetimeIndex([]), date_range_htf(cal, "D", "2020-01-01", "2020-01-01"))

    # Following should test that _days_per_week doesn't underestimate? i think?
    assert_index_equal(reference[0:1], date_range_htf(cal, "D", "2020-01-01", "2020-01-02"))
    assert_index_equal(reference[0:5], date_range_htf(cal, "D", "2020-01-01", "2020-01-08"))
    assert_index_equal(reference[0:5:2], date_range_htf(cal, "2D", "2020-01-01", "2020-01-08"))


def test_date_range_htf_weeks():
    cal = FakeCalendar().holidays()

    # region closed == 'right'
    reference = pd.DatetimeIndex(
        [
            "2025-01-03",
            "2025-01-10",
            "2025-01-17",
            "2025-01-24",
            "2025-01-31",
            "2025-02-07",
            "2025-02-14",
            "2025-02-21",
            "2025-02-28",
            "2025-03-07",
            "2025-03-14",
            "2025-03-21",
            "2025-03-28",
            "2025-04-04",
            "2025-04-11",
            "2025-04-18",
            "2025-04-25",
            "2025-05-02",
            "2025-05-09",
            "2025-05-16",
            "2025-05-23",
            "2025-05-30",
            "2025-06-06",
            "2025-06-13",
            "2025-06-20",
            "2025-06-27",
            "2025-07-04",
            "2025-07-11",
            "2025-07-18",
            "2025-07-25",
            "2025-08-01",
            "2025-08-08",
            "2025-08-15",
            "2025-08-22",
            "2025-08-29",
            "2025-09-05",
            "2025-09-12",
            "2025-09-19",
            "2025-09-26",
            "2025-10-03",
            "2025-10-10",
            "2025-10-17",
            "2025-10-24",
            "2025-10-31",
            "2025-11-07",
            "2025-11-14",
            "2025-11-21",
            "2025-11-28",
            "2025-12-05",
            "2025-12-12",
            "2025-12-19",
            "2025-12-26",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "1W", "2025-01-01", "2026-01-01"))

    assert_index_equal(reference[::2], date_range_htf(cal, "2W", "2025-01-01", "2026-01-01"))
    assert_index_equal(reference[::5], date_range_htf(cal, "5W", "2025-01-03", "2026-01-01"))
    assert_index_equal(reference[1::5], date_range_htf(cal, "5W", "2025-01-04", "2026-01-01"))
    assert_index_equal(reference[:20], date_range_htf(cal, "W", "2025-01-01", None, 20))
    assert_index_equal(reference[-20:], date_range_htf(cal, "W", None, "2026-01-01", 20))
    assert_index_equal(pd.DatetimeIndex([]), date_range_htf(cal, "W", "2020-01-01", "2020-01-02"))

    # endregion
    # region closed == 'left'
    reference = pd.DatetimeIndex(
        [
            "2025-01-06",
            "2025-01-13",
            "2025-01-20",
            "2025-01-27",
            "2025-02-03",
            "2025-02-10",
            "2025-02-17",
            "2025-02-24",
            "2025-03-03",
            "2025-03-10",
            "2025-03-17",
            "2025-03-24",
            "2025-03-31",
            "2025-04-07",
            "2025-04-14",
            "2025-04-21",
            "2025-04-28",
            "2025-05-05",
            "2025-05-12",
            "2025-05-19",
            "2025-05-26",
            "2025-06-02",
            "2025-06-09",
            "2025-06-16",
            "2025-06-23",
            "2025-06-30",
            "2025-07-07",
            "2025-07-14",
            "2025-07-21",
            "2025-07-28",
            "2025-08-04",
            "2025-08-11",
            "2025-08-18",
            "2025-08-25",
            "2025-09-01",
            "2025-09-08",
            "2025-09-15",
            "2025-09-22",
            "2025-09-29",
            "2025-10-06",
            "2025-10-13",
            "2025-10-20",
            "2025-10-27",
            "2025-11-03",
            "2025-11-10",
            "2025-11-17",
            "2025-11-24",
            "2025-12-01",
            "2025-12-08",
            "2025-12-15",
            "2025-12-22",
            "2025-12-29",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "1W", "2025-01-01", "2026-01-01", closed="left"))

    assert_index_equal(
        reference[::2],
        date_range_htf(cal, "2W", "2025-01-01", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[::5],
        date_range_htf(cal, "5W", "2025-01-05", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[::5],
        date_range_htf(cal, "5W", "2025-01-06", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5W", "2025-01-07", "2026-01-01", closed="left"),
    )
    assert_index_equal(reference[:20], date_range_htf(cal, "W", "2025-01-01", None, 20, closed="left"))
    assert_index_equal(reference[-20:], date_range_htf(cal, "W", None, "2026-01-01", 20, closed="left"))
    assert_index_equal(
        pd.DatetimeIndex([]),
        date_range_htf(cal, "W", "2020-01-01", "2020-01-05", closed="left"),
    )
    # endregion

    assert_index_equal(  # Checks that 'WED' Anchor Rolls Closed 2025-01-01 'WED' to 2025-01-02
        pd.DatetimeIndex(
            ["2025-01-02", "2025-01-08", "2025-01-15", "2025-01-22", "2025-01-29"],
            dtype="datetime64[ns]",
            freq=None,
        ),
        date_range_htf(cal, "1W", "2025-01-01", "2025-02-01", closed="left", day_anchor="WED"),
    )
    assert_index_equal(  # Checks that 'WED' Anchor Trims off Closed 2025-01-01 'WED'
        pd.DatetimeIndex(
            ["2025-01-08", "2025-01-15", "2025-01-22", "2025-01-29"],
            dtype="datetime64[ns]",
            freq=None,
        ),
        date_range_htf(cal, "1W", "2025-01-01", "2025-02-01", closed="right", day_anchor="WED"),
    )


def test_date_range_htf_months():
    cal = FakeCalendar().holidays()

    # region closed == 'right'
    reference = pd.DatetimeIndex(
        [
            "2025-01-31",
            "2025-02-28",
            "2025-03-31",
            "2025-04-30",
            "2025-05-30",
            "2025-06-30",
            "2025-07-31",
            "2025-08-29",
            "2025-09-30",
            "2025-10-31",
            "2025-11-28",
            "2025-12-31",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "M", "2025-01-01", "2026-01-01"))

    assert_index_equal(reference[::2], date_range_htf(cal, "2M", "2025-01-01", "2026-01-01"))
    assert_index_equal(reference[4::5], date_range_htf(cal, "5M", "2025-05-30", "2026-01-01"))
    assert_index_equal(reference[5::5], date_range_htf(cal, "5M", "2025-05-31", "2026-01-01"))
    assert_index_equal(reference[:10], date_range_htf(cal, "M", "2025-01-01", None, 10))
    assert_index_equal(reference[-10:], date_range_htf(cal, "M", None, "2026-01-01", 10))
    assert_index_equal(reference[3::2], date_range_htf(cal, "2M", None, "2026-01-01", 5))
    assert_index_equal(reference[2:-1:2], date_range_htf(cal, "2M", None, "2025-12-30", 5))
    assert_index_equal(pd.DatetimeIndex([]), date_range_htf(cal, "M", "2020-01-01", "2020-01-02"))
    # endregion

    # region closed == 'left'
    reference = pd.DatetimeIndex(
        [
            "2025-01-02",
            "2025-02-03",
            "2025-03-03",
            "2025-04-01",
            "2025-05-01",
            "2025-06-02",
            "2025-07-01",
            "2025-08-01",
            "2025-09-01",
            "2025-10-01",
            "2025-11-03",
            "2025-12-01",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "1M", "2025-01-01", "2026-01-01", closed="left"))

    assert_index_equal(
        reference[::2],
        date_range_htf(cal, "2M", "2025-01-01", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[::5],
        date_range_htf(cal, "5M", "2025-01-02", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5M", "2025-01-05", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[::5],
        date_range_htf(cal, "5M", "2025-01-02", "2026-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5M", "2025-01-05", "2026-01-01", closed="left"),
    )
    assert_index_equal(reference[:10], date_range_htf(cal, "M", "2025-01-01", None, 10, closed="left"))
    assert_index_equal(reference[-10:], date_range_htf(cal, "M", None, "2026-01-01", 10, closed="left"))
    assert_index_equal(reference[3::2], date_range_htf(cal, "2M", None, "2026-01-01", 5, closed="left"))
    assert_index_equal(
        pd.DatetimeIndex([]),
        date_range_htf(cal, "M", "2020-01-01", "2020-01-01", closed="left"),
    )
    # endregion


def test_date_range_htf_quarters():
    cal = FakeCalendar().holidays()

    # region closed == 'right'
    reference = pd.DatetimeIndex(
        [
            "2025-03-31",
            "2025-06-30",
            "2025-09-30",
            "2025-12-31",
            "2026-03-31",
            "2026-06-30",
            "2026-09-30",
            "2026-12-31",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "Q", "2025-01-01", "2027-01-01"))

    assert_index_equal(reference[::2], date_range_htf(cal, "2Q", "2025-01-01", "2027-01-01"))
    assert_index_equal(reference[:5], date_range_htf(cal, "Q", "2025-01-01", None, 5))
    assert_index_equal(reference[-5:], date_range_htf(cal, "Q", None, "2027-01-01", 5))
    assert_index_equal(reference[1::2], date_range_htf(cal, "2Q", None, "2027-01-01", 4))
    assert_index_equal(reference[1::2], date_range_htf(cal, "2Q", None, "2026-12-31", 4))
    assert_index_equal(pd.DatetimeIndex([]), date_range_htf(cal, "Q", "2020-01-01", "2020-01-02"))
    # endregion

    # region closed == 'left'
    reference = pd.DatetimeIndex(
        [
            "2025-01-02",
            "2025-04-01",
            "2025-07-01",
            "2025-10-01",
            "2026-01-02",
            "2026-04-01",
            "2026-07-01",
            "2026-10-01",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "1Q", "2025-01-01", "2027-01-01", closed="left"))
    assert_index_equal(
        reference[::2],
        date_range_htf(cal, "2Q", "2025-01-01", "2027-01-01", closed="left"),
    )
    assert_index_equal(
        reference[::5],
        date_range_htf(cal, "5Q", "2025-01-02", "2027-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5Q", "2025-01-05", "2027-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5Q", "2025-01-05", "2027-01-01", closed="left"),
    )
    assert_index_equal(reference[:5], date_range_htf(cal, "Q", "2025-01-01", None, 5, closed="left"))
    assert_index_equal(reference[-5:], date_range_htf(cal, "Q", None, "2027-01-01", 5, closed="left"))
    assert_index_equal(reference[1::2], date_range_htf(cal, "2Q", None, "2027-01-01", 4, closed="left"))
    assert_index_equal(
        pd.DatetimeIndex([]),
        date_range_htf(cal, "Q", "2020-01-01", "2020-01-01", closed="left"),
    )
    # endregion

    assert_index_equal(
        pd.DatetimeIndex(
            ["2025-01-31", "2025-04-30", "2025-07-31", "2025-10-31"],
            dtype="datetime64[ns]",
            freq=None,
        ),
        date_range_htf(cal, "Q", "2025-01-01", "2026-01-01", month_anchor="FEB"),
    )
    assert_index_equal(
        pd.DatetimeIndex(
            ["2025-02-03", "2025-05-01", "2025-08-01", "2025-11-03"],
            dtype="datetime64[ns]",
            freq=None,
        ),
        date_range_htf(cal, "Q", "2025-01-01", "2026-01-01", closed="left", month_anchor="FEB"),
    )


def test_date_range_htf_years():
    cal = FakeCalendar().holidays()

    # region closed == 'right'
    reference = pd.DatetimeIndex(
        [
            "2025-12-31",
            "2026-12-31",
            "2027-12-31",
            "2028-12-29",
            "2029-12-31",
            "2030-12-31",
            "2031-12-31",
            "2032-12-31",
            "2033-12-30",
            "2034-12-29",
            "2035-12-31",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "Y", "2025-01-01", "2036-01-01"))

    assert_index_equal(reference[::2], date_range_htf(cal, "2Y", "2025-01-01", "2036-01-01"))
    assert_index_equal(reference[:5], date_range_htf(cal, "Y", "2025-01-01", None, 5))
    assert_index_equal(reference[-5:], date_range_htf(cal, "Y", None, "2036-01-01", 5))
    assert_index_equal(reference[::2], date_range_htf(cal, "2Y", None, "2036-01-01", 6))
    assert_index_equal(reference[1::2], date_range_htf(cal, "2Y", None, "2035-12-30", 5))
    assert_index_equal(pd.DatetimeIndex([]), date_range_htf(cal, "Y", "2020-01-01", "2020-01-02"))
    # endregion

    # region closed == 'left'
    reference = pd.DatetimeIndex(
        [
            "2025-01-02",
            "2026-01-02",
            "2027-01-04",
            "2028-01-03",
            "2029-01-02",
            "2030-01-02",
            "2031-01-02",
            "2032-01-02",
            "2033-01-03",
            "2034-01-03",
            "2035-01-02",
        ],
        dtype="datetime64[ns]",
        freq=None,
    )

    assert_index_equal(reference, date_range_htf(cal, "1Y", "2025-01-01", "2036-01-01", closed="left"))
    assert_index_equal(
        reference[::2],
        date_range_htf(cal, "2Y", "2025-01-01", "2036-01-01", closed="left"),
    )
    assert_index_equal(
        reference[::5],
        date_range_htf(cal, "5Y", "2025-01-02", "2036-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5Y", "2025-01-05", "2036-01-01", closed="left"),
    )
    assert_index_equal(
        reference[1::5],
        date_range_htf(cal, "5Y", "2025-01-05", "2036-01-01", closed="left"),
    )
    assert_index_equal(reference[:5], date_range_htf(cal, "Y", "2025-01-01", None, 5, closed="left"))
    assert_index_equal(reference[-6:], date_range_htf(cal, "Y", None, "2036-01-01", 6, closed="left"))
    assert_index_equal(reference[2::2], date_range_htf(cal, "2Y", None, "2036-01-01", 5, closed="left"))
    assert_index_equal(
        pd.DatetimeIndex([]),
        date_range_htf(cal, "Y", "2020-01-01", "2020-01-01", closed="left"),
    )

    assert_index_equal(
        pd.DatetimeIndex(
            ["2025-01-31", "2026-01-30", "2027-01-29"],
            dtype="datetime64[ns]",
            freq=None,
        ),
        date_range_htf(cal, "Y", "2025-01-01", "2028-01-01", month_anchor="FEB"),
    )
    assert_index_equal(
        pd.DatetimeIndex(
            ["2025-02-03", "2026-02-02", "2027-02-01"],
            dtype="datetime64[ns]",
            freq=None,
        ),
        date_range_htf(cal, "Y", "2025-01-01", "2028-01-01", closed="left", month_anchor="FEB"),
    )
    # endregion


# endregion
