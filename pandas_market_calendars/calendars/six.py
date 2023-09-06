from datetime import time

from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    Day,
    Easter,
    EasterMonday,
    GoodFriday,
    Holiday,
    previous_friday,
)
from pytz import timezone

from pandas_market_calendars.market_calendar import (
    FRIDAY,
    MONDAY,
    MarketCalendar,
    THURSDAY,
    TUESDAY,
    WEDNESDAY,
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
    "Ascension Day",
    month=1,
    day=1,
    offset=[Easter(), Day(39)],
    days_of_week=(THURSDAY,),
)
# Pentecost Day (Pfingstmontag)
PentecostMonday = Holiday(
    "Pentecost Monday",
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
    "Christmas Eve",
    month=12,
    day=24,
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


class SIXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for SIX

    """

    aliases = ["SIX"]
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(17, 30)),),
    }

    @property
    def name(self):
        return "SIX"

    @property
    def tz(self):
        return timezone("Europe/Zurich")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
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
                BoxingDay,
                NewYearsEve,
            ]
        )
