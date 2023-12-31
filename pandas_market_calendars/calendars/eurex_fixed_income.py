from datetime import time

from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    EasterMonday,
    GoodFriday,
    Holiday,
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
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
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
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)
# New Year's Eve
NewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
)


class EUREXFixedIncomeCalendar(MarketCalendar):
    """
    Trading calendar available here:
    https://www.eurex.com/resource/blob/3378814/910cf372738890f691bc1bfbccfd3aef/data/tradingcalendar_2023_en.pdf
    """

    aliases = ["EUREX_Bond"]

    regular_market_times = {
        "market_open": ((None, time(1, 10)), ("2018-12-10", time(8, 0))),
        "market_close": ((None, time(22)),),
    }

    @property
    def name(self):
        return "EUREX_Bond"

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
                ChristmasEve,
                Christmas,
                BoxingDay,
                NewYearsEve,
            ]
        )
