#
# kewlfft
#

from datetime import time
from pandas.tseries.holiday import (
    Holiday,
    DateOffset,
    MO,
    weekend_to_monday, previous_friday,
    GoodFriday,
    EasterMonday,
)
from pytz import timezone
from pandas.tseries.holiday import AbstractHolidayCalendar
from .market_calendar import (
    MarketCalendar,
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY
)

# New Year's Eve
EUREXNewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    observance=previous_friday,
)
# New Year's Day
EUREXNewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)

# Christmas Eve
ChristmasEve = Holiday(
    'Christmas Eve',
    month=12,
    day=24,
    observance=previous_friday,
)
# Christmas
Christmas = Holiday(
    "Christmas",
    month=12,
    day=25,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)

# Boxing day
BoxingDay = Holiday(
    "Boxing Day",
    month=12,
    day=26,
)
# If boxing day is saturday then Monday 28th is a holiday
# If boxing day is sunday then Tuesday 28th is a holiday
WeekendBoxingDay = Holiday(
    "Weekend Boxing Day",
    month=12,
    day=28,
    days_of_week=(MONDAY, TUESDAY),
)


class EUREXRelaxedExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for the London Stock Exchange. Removes extra holidays.

    Open Time: 8:00 AM, GMT
    Close Time: 4:30 PM, GMT

    Regularly-Observed Holidays:
    - New Years Day (observed on first business day on/after)
    - Good Friday
    - Easter Monday
    - Early May Bank Holiday (first Monday in May)
    - Spring Bank Holiday (last Monday in May)
    - Summer Bank Holiday (last Monday in August)
    - Christmas Day
    - Dec. 27th (if Christmas is on a weekend)
    - Boxing Day
    - Dec. 28th (if Boxing Day is on a weekend)
    """

    @property
    def name(self):
        return "EUREX_RELAXED"

    @property
    def tz(self):
        return timezone('Europe/London')

    @property
    def open_time(self):
        return time(8, 0)

    @property
    def close_time(self):
        return time(16, 30)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            EUREXNewYearsDay,
            GoodFriday,
            EasterMonday,
            Christmas,
            BoxingDay,
            WeekendBoxingDay
        ])

    @property
    def special_closes(self):
        return [(
            time(12, 30),
            AbstractHolidayCalendar(rules=[
                ChristmasEve,
                EUREXNewYearsEve,
            ])
        )]
