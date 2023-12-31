from datetime import time
from itertools import chain

import pandas as pd
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
    Holiday,
)
from pytz import timezone

from pandas_market_calendars.holidays.us import (
    Christmas,
    USBlackFridayInOrAfter1993,
    USIndependenceDay,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNewYearsDay,
    HurricaneSandyClosings,
    USNationalDaysofMourning,
    USJuneteenthAfter2022,
)
from pandas_market_calendars.market_calendar import MarketCalendar


def good_friday_unless_christmas_nye_friday(dt):
    """
    Good Friday is a valid trading day if Christmas Day or New Years Day fall
    on a Friday.
    """
    if isinstance(dt, pd.DatetimeIndex):
        # Pandas < 2.1.0 will call with an index and fall-back to element by element
        # Pandas == 2.1.0 will only call element by element
        raise NotImplementedError()

    year = dt.year
    christmas_weekday = Christmas.observance(
        pd.Timestamp(year=year, month=12, day=25)
    ).weekday()
    nyd_weekday = USNewYearsDay.observance(
        pd.Timestamp(year=year, month=1, day=1)
    ).weekday()
    if christmas_weekday != 4 and nyd_weekday != 4:
        return GoodFriday.dates(
            pd.Timestamp(year=year, month=1, day=1),
            pd.Timestamp(year=year, month=12, day=31),
        )[0]
    else:
        # Not a holiday so use NaT to ensure it gets removed
        return pd.NaT


GoodFridayUnlessChristmasNYEFriday = Holiday(
    name="Good Friday CFE",
    month=1,
    day=1,
    observance=good_friday_unless_christmas_nye_friday,
)


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
    def tz(self):
        return timezone("America/Chicago")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                GoodFridayUnlessChristmasNYEFriday,
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


class CBOEIndexOptionsExchangeCalendar(CFEExchangeCalendar):
    name = "CBOE_Index_Options"
    aliases = [name]
    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(15, 15)),),
    }
