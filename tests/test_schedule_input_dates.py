import pandas as pd
from pandas.testing import assert_frame_equal, assert_index_equal

from pandas_market_calendars import calendar_registry


def test_schedule_from_days_ignores_nanosecond_time() -> None:
    calendar = calendar_registry.get_calendar("NYSE")
    days = pd.DatetimeIndex(["2024-07-03 12:34:56", "2024-07-05 15:45:12"]).as_unit("ns")
    original = days.copy()
    expected = calendar.schedule("2024-07-03", "2024-07-05")

    result = calendar.schedule_from_days(days)

    # The date-based schedule includes the July 3 early close and omits July 4.
    assert_frame_equal(result, expected, check_dtype=False, check_index_type=False)
    assert_index_equal(days, original)


def test_schedule_from_days_preserves_resolution_and_timezone_controls() -> None:
    calendar = calendar_registry.get_calendar("NYSE")
    expected = calendar.schedule("2024-07-03", "2024-07-05")
    for timezone in (None, "America/New_York"):
        for resolution in ("ns", "us"):
            days = pd.DatetimeIndex(["2024-07-03", "2024-07-05"], tz=timezone).as_unit(resolution)
            original = days.copy()
            result = calendar.schedule_from_days(days)
            assert_frame_equal(result, expected, check_dtype=False, check_index_type=False)
            assert_index_equal(days, original)

    # The timezone's local dates are retained, even when UTC dates would differ.
    days = pd.DatetimeIndex(["2024-07-03 23:45", "2024-07-05 23:45"], tz="America/New_York")
    result = calendar.schedule_from_days(days)
    assert_frame_equal(result, expected, check_dtype=False, check_index_type=False)

    days = pd.DatetimeIndex(["2024-07-03 12:34:56", "2024-07-05 15:45:12"]).as_unit("us")
    result = calendar.schedule_from_days(days)
    assert_frame_equal(result, expected, check_dtype=False, check_index_type=False)
