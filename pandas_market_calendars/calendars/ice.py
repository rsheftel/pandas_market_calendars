from datetime import time
from itertools import chain

from pandas import Timestamp
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
)
import sys 
# check python versiOn aNd import accordingly
if sys.version_info >= (3, 9):
    # For Python 3.9 and later, import directly
    from zoneinfo import ZoneInfo
else:
    # For Python 3.8 and earlier, import from backports
    from backports.zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.us import (
    Christmas,
    USIndependenceDay,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNationalDaysofMourning,
    USNewYearsDay,
)
from pandas_market_calendars.market_calendar import MarketCalendar


class ICEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for ICE US.

    Open Time: 8pm, US/Eastern
    Close Time: 6pm, US/Eastern

    https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf # noqa
    """

    aliases = ["ICE", "ICEUS", "NYFE"]
    regular_market_times = {
        "market_open": ((None, time(20, 1), -1),),  # offset by -1 day
        "market_close": ((None, time(18)),),
    }

    @property
    def name(self):
        return "ICE"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def special_closes(self):
        return [
            (
                time(13),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        USMemorialDay,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                    ]
                ),
            )
        ]

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                USNationalDaysofMourning,
                # ICE was only closed on the first day of the Hurricane Sandy
                # closings (was not closed on 2012-10-30)
                [Timestamp("2012-10-29", tz="UTC")],
            )
        )

    @property
    def regular_holidays(self):
        # https://www.theice.com/publicdocs/futures_us/exchange_notices/NewExNot2016Holidays.pdf # noqa
        return AbstractHolidayCalendar(rules=[USNewYearsDay, GoodFriday, Christmas])
