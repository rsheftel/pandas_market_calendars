from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, DateOffset, GoodFriday, Holiday, MO, weekend_to_monday
from pytz import timezone

from .holidays_uk import BoxingDay, WeekendBoxingDay, WeekendChristmas
from .holidays_us import Christmas
from .market_calendar import MarketCalendar

# New Year's Day
TSXNewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    observance=weekend_to_monday,
)
# Ontario Family Day
FamilyDay = Holiday(
    "Family Day",
    month=2,
    day=1,
    offset=DateOffset(weekday=MO(3)),
    start_date='2008-01-01',
)
# Victoria Day
# https://www.timeanddate.com/holidays/canada/victoria-day
VictoriaDay = Holiday(
    'Victoria Day',
    month=5,
    day=24,
    offset=DateOffset(weekday=MO(-1)),
)
# Canada Day
CanadaDay = Holiday(
    'Canada Day',
    month=7,
    day=1,
    observance=weekend_to_monday,
)
# Civic Holiday
CivicHoliday = Holiday(
    'Civic Holiday',
    month=8,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)
# Labor Day
LaborDay = Holiday(
    'Labor Day',
    month=9,
    day=1,
    offset=DateOffset(weekday=MO(1)),
)
# Thanksgiving
Thanksgiving = Holiday(
    'Thanksgiving',
    month=10,
    day=1,
    offset=DateOffset(weekday=MO(2)),
)


class TSXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for the Toronto Stock Exchange

    Open Time: 9:30 AM, EST
    Close Time: 4:00 PM, EST

    Regularly-Observed Holidays:
    - New Years Day (observed on first business day on/after)
    - Family Day (Third Monday in February after 2008)
    - Good Friday
    - Victoria Day (Monday before May 25th)
    - Canada Day (July 1st, observed first business day after)
    - Civic Holiday (First Monday in August)
    - Labor Day (First Monday in September)
    - Thanksgiving (Second Monday in October)
    - Christmas Day
    - Dec. 27th (if Christmas is on a weekend)
    - Boxing Day
    - Dec. 28th (if Boxing Day is on a weekend)
    """
    aliases = ['TSX', 'TSXV']

    @property
    def name(self):
        return "TSX"

    @property
    def tz(self):
        return timezone('Canada/Eastern')

    @property
    def open_time_default(self):
        return time(9, 30, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(16, tzinfo=self.tz)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            TSXNewYearsDay,
            FamilyDay,
            GoodFriday,
            VictoriaDay,
            CanadaDay,
            CivicHoliday,
            LaborDay,
            Thanksgiving,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay
        ])
