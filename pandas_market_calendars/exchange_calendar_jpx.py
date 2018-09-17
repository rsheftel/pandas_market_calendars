from datetime import time

from dateutil.relativedelta import MO
from pandas import DateOffset
from pandas.tseries.holiday import Holiday, sunday_to_monday
from pytz import timezone

from pandas.tseries.holiday import AbstractHolidayCalendar
from pandas_market_calendars.us_holidays import USNewYearsDay

from pandas_market_calendars import MarketCalendar
from pandas_market_calendars.jpx_equinox import autumnal_equinox, vernal_equinox


class JPXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for JPX

    Open Time: 9:31 AM, Asia/Tokyo
    LUNCH BREAK :facepalm: : 11:30 AM - 12:30 PM Asia/Tokyo
    Close Time: 4:00 PM, Asia/Tokyo
    """
    aliases = ['JPX']

    regular_early_close = time(13)
    lunch_start = time(11, 30)
    lunch_end = time(12, 30)

    @property
    def name(self):
        return "JPX"

    @property
    def tz(self):
        return timezone('Asia/Tokyo')

    @property
    def open_time_default(self):
        return time(9, 0, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(15, tzinfo=self.tz)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            Holiday(
                name="New Year's Day",
                month=1,
                day=2,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="New Year's Day",
                month=1,
                day=3,
                observance=sunday_to_monday,
            ),
            Holiday(  # second monday of january
                name="Coming of Age Day",
                month=1,
                day=1,
                offset=DateOffset(weekday=MO(2)),
            ),
            Holiday(
                name="National foundation day",
                month=2,
                day=11,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Vernal Equinox",
                month=3,
                day=20,
                observance=vernal_equinox
            ),
            Holiday(
                name="Showa day",
                month=4,
                day=29,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Constitution memorial day",
                month=5,
                day=3,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Greenery day",
                month=5,
                day=4,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Children's day",
                month=5,
                day=5,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Marine day",
                month=7,
                day=1,
                offset=DateOffset(weekday=MO(3)),
            ),
            Holiday(
                name="Mountain day",
                month=8,
                day=11,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Respect for the aged day",
                month=9,
                day=1,
                offset=DateOffset(weekday=MO(3)),
            ),
            Holiday(
                name="Autumnal equinox",
                month=9,
                day=22,
                observance=autumnal_equinox,
            ),
            Holiday(
                name="Health and sports day",
                month=10,
                day=1,
                offset=DateOffset(weekday=MO(2)),
            ),
            Holiday(
                name="Culture day",
                month=11,
                day=3,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Labor Thanksgiving Day",
                month=11,
                day=23,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Emperor's Birthday",
                month=12,
                day=23,
                observance=sunday_to_monday,
            ),
            Holiday(
                name="Before New Year's Day",
                month=12,
                day=31,
                observance=sunday_to_monday,
            ),
        ])

    @staticmethod
    def open_at_time(schedule, timestamp, include_close=False):
        if JPXExchangeCalendar.lunch_start < timestamp.time() < JPXExchangeCalendar.lunch_end:
            return False
        return MarketCalendar.open_at_time(schedule, timestamp, include_close)
