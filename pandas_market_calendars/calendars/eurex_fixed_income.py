from datetime import time
from typing import Any
from zoneinfo import ZoneInfo

from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    EasterMonday,
    GoodFriday,
    Holiday,
)

from pandas_market_calendars.market_calendar import (
    FRIDAY,
    MONDAY,
    THURSDAY,
    TUESDAY,
    WEDNESDAY,
    MarketCalendar,
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

    # Eurex moved the open of the Bund, Bobl, Schatz and Buxl futures forward
    # from 08:00 to the Asian time zone on Monday, 10 December 2018 (circular 063/18):
    # https://www.eurex.com/ex-en/find/circulars/No.-063-18-Extension-of-trading-hours-for-selected-benchmark-futures-and-MSCI-futures-219526
    # https://www.eurex.com/ex-en/support/initiatives/archive/trading-hour-extension
    regular_market_times = {
        "market_open": ((None, time(8, 0)), ("2018-12-10", time(1, 10))),
        "market_close": ((None, time(22)),),
    }

    @property
    def name(self) -> str:
        return "EUREX_Bond"

    @property
    def tz(self) -> Any:
        return ZoneInfo("Europe/Berlin")

    @property
    def regular_holidays(self) -> Any:
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
