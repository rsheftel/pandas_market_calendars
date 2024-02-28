#
# kewlfft
#

from datetime import time

from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
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
# Early May bank holiday
MayBank = Holiday(
    "Early May Bank Holiday",
    month=5,
    day=1,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)
# Christmas Eve
ChristmasEve = Holiday(
    "Christmas Eve",
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


class EUREXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for EUREX

    """

    aliases = ["EUREX"]
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(17, 30)),),
    }

    @property
    def name(self):
        return "EUREX"

    @property
    def tz(self):
        return timezone("Europe/Berlin")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                EUREXNewYearsDay,
                GoodFriday,
                EasterMonday,
                MayBank,
                Christmas,
                WeekendChristmas,
                BoxingDay,
                WeekendBoxingDay,
            ]
        )

    @property
    def special_closes(self):
        return [
            (
                time(12, 30),
                AbstractHolidayCalendar(
                    rules=[
                        ChristmasEve,
                        EUREXNewYearsEve,
                    ]
                ),
            )
        ]
