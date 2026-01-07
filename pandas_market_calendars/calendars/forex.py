import sys
from datetime import time

if sys.version_info >= (3, 9):
    from zoneinfo import ZoneInfo
else:
    from backports.zoneinfo import ZoneInfo

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
    def name(self):
        return "FOREX"

    @property
    def tz(self):
        return ZoneInfo("America/New_York")

    @property
    def weekmask(self):
        return "Sun Mon Tue Wed Thu Fri"
