from datetime import time
from typing import Any
from zoneinfo import ZoneInfo

from pandas_market_calendars.market_calendar import MarketCalendar


class ForexExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for Forex (FX) market.

    Trading hours: Sunday 5:00 PM EST/EDT to Friday 5:00 PM EST/EDT.
    Closed on Saturdays, no holidays.
    """

    aliases = ["FOREX", "FX", "Forex"]

    regular_market_times = {
        "market_open": ((None, time(17, 0), -1),),
        "market_close": ((None, time(17, 0)),),
    }

    @property
    def name(self) -> str:
        return "FOREX"

    @property
    def tz(self) -> Any:
        return ZoneInfo("America/New_York")

    @property
    def weekmask(self) -> str:
        # Monday's session already opens Sunday 17:00 through the -1 open offset.
        # A Sunday session date would open Saturday 17:00, during the weekend
        # close that runs from Friday 17:00 until Sunday 17:00.
        return "Mon Tue Wed Thu Fri"
