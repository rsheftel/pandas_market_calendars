import pandas as pd
import pandas.testing as tm
import pytest

from tests import conftest


DAILY = pd.date_range("2024-01-01", periods=3, freq="D")
NO_FREQ = pd.DatetimeIndex(DAILY, freq=None)


def test_assert_index_equal_ignores_freq_by_default():
    tm.assert_index_equal(DAILY, NO_FREQ)
    tm.assert_index_equal(NO_FREQ, DAILY)


def test_assert_index_equal_checks_freq_when_requested():
    tm.assert_index_equal(DAILY, DAILY.copy(), check_freq=True)

    with pytest.raises(AssertionError, match="freq"):
        tm.assert_index_equal(DAILY, NO_FREQ, check_freq=True)


def test_assert_index_equal_detects_value_differences():
    shifted = DAILY + pd.Timedelta(days=1)

    with pytest.raises(AssertionError):
        tm.assert_index_equal(DAILY, shifted)
    with pytest.raises(AssertionError):
        tm.assert_index_equal(DAILY, DAILY[:2])


def test_assert_index_equal_normalizes_datetime_resolution():
    tm.assert_index_equal(NO_FREQ.as_unit("ns"), NO_FREQ.as_unit("s"))
    tm.assert_index_equal(DAILY.as_unit("ns"), DAILY.as_unit("us"), check_freq=True)


def test_assert_index_equal_emulates_check_freq_without_pandas_support(monkeypatch):
    # Simulate pandas < 3.1, whose assert_index_equal has no check_freq parameter and ignores freq
    original = conftest._original_assert_index_equal
    original_supports_check_freq = conftest._INDEX_SUPPORTS_CHECK_FREQ

    def legacy_assert_index_equal(left, right, **kwargs):
        assert "check_freq" not in kwargs
        if original_supports_check_freq:
            kwargs["check_freq"] = False
        original(left, right, **kwargs)

    monkeypatch.setattr(conftest, "_INDEX_SUPPORTS_CHECK_FREQ", False)
    monkeypatch.setattr(conftest, "_original_assert_index_equal", legacy_assert_index_equal)

    tm.assert_index_equal(DAILY, NO_FREQ)
    tm.assert_index_equal(DAILY, DAILY.copy(), check_freq=True)
    with pytest.raises(AssertionError, match="freq"):
        tm.assert_index_equal(DAILY, NO_FREQ, check_freq=True)
    with pytest.raises(AssertionError):
        tm.assert_index_equal(DAILY, DAILY + pd.Timedelta(days=1), check_freq=True)
