"""Binary weekmasks count only open days when estimating calendar ranges."""

import pytest

from pandas_market_calendars import calendar_utils


@pytest.mark.parametrize(
    "mask, expected",
    [
        ("1111100", 5),
        ("1000000", 1),
        ("0000000", 0),
        ("1111111", 7),
        ("Mon Wed Fri", 3),
        ([True, False, False, False, False, False, True], 2),
    ],
)
def test_days_per_week(mask, expected: int) -> None:
    assert calendar_utils._days_per_week(mask) == expected
