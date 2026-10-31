#
# kewlfft
#
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


# New Year's Eve
EUREXNewYearsEve = Holiday(
    "New Year's Eve",
    month=12,
    day=31,
    days_of_week=(MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY),
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
)


class EUREXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for EUREX

    """

    aliases = ["EUREX"]
    regular_market_times = {
        "market_open": ((None, time(8)),),
        "market_close": ((None, time(22)),),
    }

    @property
    def name(self) -> str:
        return "EUREX"

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
                EUREXNewYearsEve,
            ]
        )


class EUREXPrePostExchangeCalendar(EUREXExchangeCalendar):
    """
    EUREX calendar variant with explicit pre and post sessions.

    Issue #184 requested these session endpoints in UTC. This calendar keeps
    those endpoints in UTC instead of interpreting them as Europe/Berlin wall
    times, which would shift them across daylight-saving transitions.
    """

    aliases = ["EUREX_PrePost", "EUREX_Extended"]

    regular_market_times = {
        "pre": ((None, time(0, 15)),),
        "market_open": ((None, time(8)),),
        "market_close": ((None, time(16, 30)),),
        "post": ((None, time(21)),),
    }

    @property
    def name(self) -> str:
        return "EUREX_PrePost"

    @property
    def tz(self) -> Any:
        return ZoneInfo("UTC")
