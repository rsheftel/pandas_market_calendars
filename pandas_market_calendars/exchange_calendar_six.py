from datetime import time
from pandas.tseries.holiday import (
    Holiday,
    previous_friday,
    GoodFriday,
    EasterMonday,
    Easter,
    AbstractHolidayCalendar,
    Day,
)
from pytz import timezone
from .market_calendar import (
    MarketCalendar,
    MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY,
)

# New Year's Eve
NewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    observance=previous_friday,
)
# New Year's Day
NewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)
# Berthold's Day
BertholdsDay = Holiday(
    "Berthold's Day",
    month=1,
    day=2,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)
# Early May bank holiday
MayBank = Holiday(
    "Early May Bank Holiday",
    month=5,
    day=1,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)
# Ascension Day (Auffahrt)
AscensionDay = Holiday(
    'Ascension Day',
    month=1,
    day=1,
    offset=[Easter(), Day(39)],
    days_of_week=(THURSDAY,),
)
# Pentecost Day (Pfingstmontag)
PentecostMonday = Holiday(
    'Pentecost Monday',
    month=1,
    day=1,
    offset=[Easter(), Day(50)],
    days_of_week=(MONDAY,),
)
# Swiss National Day
SwissNationalDay = Holiday(
    "Swiss National Day",
    month=8,
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
# If christmas day is Saturday Monday 27th is a holiday
# If christmas day is sunday the Tuesday 27th is a holiday
WeekendChristmas = Holiday(
    "Weekend Christmas",
    month=12,
    day=27,
    days_of_week=(MONDAY, TUESDAY),
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


class SIXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for SIX

    """
    aliases = ['SIX']

    @property
    def name(self):
        return "SIX"

    @property
    def tz(self):
        return timezone('Europe/Zurich')

    @property
    def open_time_default(self):
        return time(9, 0, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(17, 30, tzinfo=self.tz)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            NewYearsDay,
            BertholdsDay,
            GoodFriday,
            EasterMonday,
            MayBank,
            AscensionDay,
            PentecostMonday,
            SwissNationalDay,
            ChristmasEve,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay,
            NewYearsEve,
        ])

#    @property
#    def special_closes(self):
#        return [(
#            time(12, 30),
#            AbstractHolidayCalendar(rules=[
#                ChristmasEve,
#                NewYearsEve,
#            ])
#        )]
