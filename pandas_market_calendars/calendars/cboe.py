from datetime import time
from itertools import chain

import pandas as pd
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
)
from zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.us import (
    Christmas,
    FridayAfterIndependenceDayPre2013,
    HurricaneSandyClosings,
    MonTuesThursBeforeIndependenceDay,
    USBlackFridayInOrAfter1993,
    USIndependenceDay,
    USJuneteenthAfter2022,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNationalDaysofMourning,
    USNewYearsDay,
    WednesdayBeforeIndependenceDayPost2013,
)
from pandas_market_calendars.market_calendar import MarketCalendar


class CFEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for the CBOE Futures Exchange (CFE).

    http://cfe.cboe.com/aboutcfe/expirationcalendar.aspx

    Open Time: 8:30am, America/Chicago
    Close Time: 3:15pm, America/Chicago

    (We are ignoring extended trading hours for now)
    """

    aliases = ["CFE", "CBOE_Futures"]
    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(15, 15)),),
    }

    @property
    def name(self):
        return "CFE"

    @property
    def full_name(self):
        return "CBOE Futures Exchange"

    @property
    def tz(self):
        return ZoneInfo("America/Chicago")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                GoodFriday,
                USJuneteenthAfter2022,
                USIndependenceDay,
                USMemorialDay,
                USLaborDay,
                USThanksgivingDay,
                Christmas,
            ]
        )

    @property
    def special_closes(self):
        return [
            (
                time(12, 15),
                AbstractHolidayCalendar(
                    rules=[
                        MonTuesThursBeforeIndependenceDay,
                        FridayAfterIndependenceDayPre2013,
                        WednesdayBeforeIndependenceDayPost2013,
                        USBlackFridayInOrAfter1993,
                    ]
                ),
            )
        ]

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                HurricaneSandyClosings,
                USNationalDaysofMourning,
            )
        )


class CBOEEquityOptionsExchangeCalendar(CFEExchangeCalendar):
    name = "CBOE_Equity_Options"
    aliases = [name]
    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(15)),),
    }

    @property
    def special_closes(self):
        return [
            (
                time(12),
                AbstractHolidayCalendar(
                    rules=[
                        MonTuesThursBeforeIndependenceDay,
                        FridayAfterIndependenceDayPre2013,
                        WednesdayBeforeIndependenceDayPost2013,
                        USBlackFridayInOrAfter1993,
                    ]
                ),
            )
        ]


class CBOEIndexOptionsExchangeCalendar(CFEExchangeCalendar):
    name = "CBOE_Index_Options"
    aliases = [name]
    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(15, 15)),),
    }
