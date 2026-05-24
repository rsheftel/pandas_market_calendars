import subprocess
import sys
import textwrap


def test_import_does_not_change_pandas_holiday_calendar_defaults():
    code = textwrap.dedent(
        """
        import pandas as pd
        from pandas.tseries.holiday import MO, AbstractHolidayCalendar, Holiday
        from pandas.tseries.offsets import CustomBusinessDay

        USMemorialDay = Holiday(
            "Memorial Day", month=5, day=31, offset=pd.DateOffset(weekday=MO(-1))
        )

        class ExampleCalendar(AbstractHolidayCalendar):
            rules = [USMemorialDay]

        bday_before = CustomBusinessDay(calendar=ExampleCalendar())
        baseline_start = AbstractHolidayCalendar.start_date
        baseline_end = AbstractHolidayCalendar.end_date

        import pandas_market_calendars
        from pandas_market_calendars.market_calendar import HolidayCalendar

        bounded = HolidayCalendar(rules=[USMemorialDay], start_date="2010-01-01", end_date="2010-12-31")
        bounded_holidays = bounded.holidays()
        bday_after = CustomBusinessDay(calendar=ExampleCalendar())

        assert bday_before == bday_after
        assert bounded_holidays[0] == pd.Timestamp("2010-05-31")
        assert AbstractHolidayCalendar.start_date == baseline_start
        assert AbstractHolidayCalendar.end_date == baseline_end
        """
    )

    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        check=False,
        text=True,
    )

    assert result.returncode == 0, result.stderr
