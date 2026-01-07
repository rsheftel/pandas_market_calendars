"""
Test that importing pandas_market_calendars does not mutate pandas' AbstractHolidayCalendar.
"""

import pandas as pd
from pandas.tseries.holiday import MO, AbstractHolidayCalendar, Holiday
from pandas.tseries.offsets import CustomBusinessDay


def test_importing_does_not_mutate_abstract_holiday_calendar():
    """
    Test that importing pandas_market_calendars does not change the global
    AbstractHolidayCalendar.start_date attribute.

    This test verifies that CustomBusinessDay objects created before and after
    importing pandas_market_calendars are equal.
    """
    # Store the original start_date
    original_start_date = AbstractHolidayCalendar.start_date

    # Create a custom calendar
    USMemorialDay = Holiday("Memorial Day", month=5, day=31, offset=pd.DateOffset(weekday=MO(-1)))

    class ExampleCalendar(AbstractHolidayCalendar):
        rules = [USMemorialDay]

    # Create business day objects before any import side effects
    bday1 = CustomBusinessDay(calendar=ExampleCalendar())
    bday2 = CustomBusinessDay(calendar=ExampleCalendar())

    # These should be equal
    assert bday1 == bday2

    # Import pandas_market_calendars - this should not mutate AbstractHolidayCalendar
    import pandas_market_calendars  # noqa: F401

    # Verify start_date is unchanged
    assert AbstractHolidayCalendar.start_date == original_start_date, (
        f"AbstractHolidayCalendar.start_date was changed from {original_start_date} "
        f"to {AbstractHolidayCalendar.start_date} after importing pandas_market_calendars"
    )

    # Create a new business day object after the import
    bday3 = CustomBusinessDay(calendar=ExampleCalendar())

    # This should still be equal to the original business day objects
    assert bday1 == bday3, (
        "CustomBusinessDay objects created before and after importing " "pandas_market_calendars should be equal"
    )


def test_nyse_calendar_has_correct_start_date():
    """
    Test that NYSE calendar internally uses the correct start_date (1885-01-01)
    without affecting the global AbstractHolidayCalendar.
    """
    import pandas_market_calendars as mcal

    # Verify global AbstractHolidayCalendar is not affected
    assert str(AbstractHolidayCalendar.start_date) == "1970-01-01 00:00:00"

    # Get NYSE calendar and verify it works correctly
    nyse = mcal.get_calendar("NYSE")

    # The regular_holidays should have the correct start_date
    assert str(nyse.regular_holidays.start_date) == "1885-01-01"

    # But global AbstractHolidayCalendar should still be unchanged
    assert str(AbstractHolidayCalendar.start_date) == "1970-01-01 00:00:00"


def test_asx_calendar_has_correct_start_date():
    """
    Test that ASX calendar internally uses the correct start_date (2011-01-01)
    without affecting the global AbstractHolidayCalendar.
    """
    import pandas_market_calendars as mcal

    # Verify global AbstractHolidayCalendar is not affected
    assert str(AbstractHolidayCalendar.start_date) == "1970-01-01 00:00:00"

    # Get ASX calendar and verify it works correctly
    asx = mcal.get_calendar("ASX")

    # The regular_holidays should have the correct start_date
    assert str(asx.regular_holidays.start_date) == "2011-01-01"

    # But global AbstractHolidayCalendar should still be unchanged
    assert str(AbstractHolidayCalendar.start_date) == "1970-01-01 00:00:00"
