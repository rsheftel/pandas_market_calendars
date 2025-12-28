"""
Tests for get_time_on, close_time_on, and open_time_on methods.

These methods should return the actual time (regular or special) for a given date.
"""

import datetime

import pandas_market_calendars as mcal
import pytest


class TestNYSETimeOnMethods:
    """Test time_on methods for NYSE calendar."""

    @pytest.fixture
    def nyse(self):
        return mcal.get_calendar("NYSE")

    def test_close_time_on_regular_day(self, nyse):
        # Regular trading day should return standard close time
        close_time = nyse.close_time_on(datetime.date(2024, 12, 2))
        assert close_time.hour == 16
        assert close_time.minute == 0

    def test_close_time_on_early_close_day_after_thanksgiving(self, nyse):
        # Day after Thanksgiving (Black Friday) - early close at 1pm
        close_time = nyse.close_time_on(datetime.date(2024, 11, 29))
        assert close_time.hour == 13
        assert close_time.minute == 0

    def test_close_time_on_early_close_christmas_eve(self, nyse):
        # Christmas Eve - early close at 1pm
        close_time = nyse.close_time_on(datetime.date(2024, 12, 24))
        assert close_time.hour == 13
        assert close_time.minute == 0

    def test_close_time_on_early_close_july_3(self, nyse):
        # July 3rd - early close at 1pm (when not Friday)
        close_time = nyse.close_time_on(datetime.date(2024, 7, 3))
        assert close_time.hour == 13
        assert close_time.minute == 0

    def test_close_time_on_multiple_years(self, nyse):
        # Test Black Friday across multiple years to ensure consistency
        close_2023 = nyse.close_time_on(datetime.date(2023, 11, 24))
        close_2024 = nyse.close_time_on(datetime.date(2024, 11, 29))
        close_2025 = nyse.close_time_on(datetime.date(2025, 11, 28))

        # All should be 1pm
        assert close_2023.hour == 13
        assert close_2024.hour == 13
        assert close_2025.hour == 13

    def test_open_time_on_regular_day(self, nyse):
        # Regular trading day should return standard open time
        open_time = nyse.open_time_on(datetime.date(2024, 12, 2))
        assert open_time.hour == 9
        assert open_time.minute == 30

    def test_close_time_on_consistency_with_schedule(self, nyse):
        # Verify close_time_on matches what schedule shows
        test_date = datetime.date(2024, 11, 29)
        close_time = nyse.close_time_on(test_date)

        # Get schedule for the same date
        schedule = nyse.schedule(start_date=test_date, end_date=test_date)
        schedule_close = schedule.loc[schedule.index[0], "market_close"]

        # Convert schedule close (UTC) to local time
        schedule_close_local = schedule_close.tz_convert(nyse.tz).time()

        # They should match
        assert close_time.hour == schedule_close_local.hour
        assert close_time.minute == schedule_close_local.minute

    def test_open_time_on_consistency_with_schedule(self, nyse):
        # Verify open_time_on matches what schedule shows
        test_date = datetime.date(2024, 12, 2)
        open_time = nyse.open_time_on(test_date)

        # Get schedule for the same date
        schedule = nyse.schedule(start_date=test_date, end_date=test_date)
        schedule_open = schedule.loc[schedule.index[0], "market_open"]

        # Convert schedule open (UTC) to local time
        schedule_open_local = schedule_open.tz_convert(nyse.tz).time()

        # They should match
        assert open_time.hour == schedule_open_local.hour
        assert open_time.minute == schedule_open_local.minute

    def test_close_time_on_with_timestamp_input(self, nyse):
        # Should work with pd.Timestamp as input
        import pandas as pd

        close_time = nyse.close_time_on(pd.Timestamp("2024-11-29"))
        assert close_time.hour == 13
        assert close_time.minute == 0

    def test_close_time_on_with_string_input(self, nyse):
        # Should work with string date as input
        close_time = nyse.close_time_on("2024-11-29")
        assert close_time.hour == 13
        assert close_time.minute == 0
