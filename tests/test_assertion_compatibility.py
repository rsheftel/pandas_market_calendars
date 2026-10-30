import pandas as pd
import pandas.testing as tm
import pytest


@pytest.mark.parametrize("freq", ["D", "B", pd.offsets.CustomBusinessDay()])
@pytest.mark.parametrize("as_frame", [False, True])
def test_datetime_assertions_allow_frequency_metadata_differences(
    freq: str | pd.offsets.CustomBusinessDay, as_frame: bool
) -> None:
    index = pd.date_range("2026-01-05", periods=3, freq=freq)
    actual = pd.Series(pd.date_range("2026-01-05", periods=3, tz="UTC"), index=index)
    expected = actual.copy()
    expected.index = pd.DatetimeIndex(list(index))
    if as_frame:
        actual, expected = actual.to_frame(), expected.to_frame()
        assertion = tm.assert_frame_equal
    else:
        assertion = tm.assert_series_equal

    assertion(actual, expected)
    assertion(actual, expected, check_freq=False)
    with pytest.raises(AssertionError, match="Day"):
        assertion(actual, expected, check_freq=True)


@pytest.mark.parametrize("as_frame", [False, True])
def test_datetime_assertions_reject_different_values(as_frame: bool) -> None:
    index = pd.date_range("2026-01-05", periods=3)
    actual = pd.Series([1, 2, 3], index=index)
    expected = pd.Series([1, 2, 4], index=pd.DatetimeIndex(list(index)))
    if as_frame:
        actual, expected = actual.to_frame(), expected.to_frame()
        assertion = tm.assert_frame_equal
    else:
        assertion = tm.assert_series_equal

    with pytest.raises(AssertionError, match="values are different"):
        assertion(actual, expected)
