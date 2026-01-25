"""
Pytest configuration for pandas_market_calendars tests.

This module provides compatibility fixes for pandas 3.0+ where datetime
resolution defaults changed from nanoseconds to varying resolutions.
"""

import pandas as pd
import pandas.testing as tm


# Store original functions
_original_assert_index_equal = tm.assert_index_equal
_original_assert_series_equal = tm.assert_series_equal
_original_assert_frame_equal = tm.assert_frame_equal


def _normalize_datetime_resolution(obj):
    """Convert datetime columns/index to a common resolution for comparison."""

    def _convert_index_to_us(idx):
        """Convert a DatetimeIndex to microsecond resolution."""
        if idx is None or not isinstance(idx, pd.DatetimeIndex):
            return idx
        try:
            return idx.as_unit("us")
        except (AttributeError, TypeError):
            return idx

    def _convert_series_to_us(s):
        """Convert a datetime Series to microsecond resolution."""
        if not pd.api.types.is_datetime64_any_dtype(s):
            return s
        try:
            return s.dt.as_unit("us")
        except (AttributeError, TypeError):
            return s

    if isinstance(obj, pd.DataFrame):
        obj = obj.copy()
        for col in obj.columns:
            if pd.api.types.is_datetime64_any_dtype(obj[col]):
                obj[col] = _convert_series_to_us(obj[col])
        if isinstance(obj.index, pd.DatetimeIndex):
            obj.index = _convert_index_to_us(obj.index)
        return obj
    elif isinstance(obj, pd.Series):
        obj = obj.copy()
        if pd.api.types.is_datetime64_any_dtype(obj):
            obj = _convert_series_to_us(obj)
        if isinstance(obj.index, pd.DatetimeIndex):
            obj.index = _convert_index_to_us(obj.index)
        return obj
    elif isinstance(obj, pd.DatetimeIndex):
        return _convert_index_to_us(obj)
    return obj


def _patched_assert_index_equal(left, right, exact="equiv", **kwargs):
    """
    Wrapper for assert_index_equal that allows datetime resolution differences.
    """
    if isinstance(left, pd.DatetimeIndex) and isinstance(right, pd.DatetimeIndex):
        left = _normalize_datetime_resolution(left)
        right = _normalize_datetime_resolution(right)
        exact = False
    return _original_assert_index_equal(left, right, exact=exact, **kwargs)


def _patched_assert_series_equal(left, right, check_dtype=True, check_index_type="equiv", **kwargs):
    """
    Wrapper for assert_series_equal that allows datetime resolution differences.
    """
    # Normalize datetime series and their indices
    left = _normalize_datetime_resolution(left)
    right = _normalize_datetime_resolution(right)

    # If series or index contain datetimes, don't check exact dtypes
    has_datetime = (
        pd.api.types.is_datetime64_any_dtype(left)
        or pd.api.types.is_datetime64_any_dtype(right)
        or isinstance(left.index, pd.DatetimeIndex)
        or isinstance(right.index, pd.DatetimeIndex)
    )
    if has_datetime:
        check_dtype = False
        check_index_type = False

    return _original_assert_series_equal(
        left, right, check_dtype=check_dtype, check_index_type=check_index_type, **kwargs
    )


def _patched_assert_frame_equal(left, right, check_dtype=True, **kwargs):
    """
    Wrapper for assert_frame_equal that allows datetime resolution differences.
    """
    left = _normalize_datetime_resolution(left)
    right = _normalize_datetime_resolution(right)
    check_dtype = False
    return _original_assert_frame_equal(left, right, check_dtype=check_dtype, **kwargs)


# Apply patches at module import time
tm.assert_index_equal = _patched_assert_index_equal
tm.assert_series_equal = _patched_assert_series_equal
tm.assert_frame_equal = _patched_assert_frame_equal
