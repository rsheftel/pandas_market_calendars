from .exchange_calendar_cme_globex_base import CMEGlobexBaseExchangeCalendar

from datetime import time
from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone

from pandas_market_calendars.holidays_cme import (
    USMartinLutherKingJrAfter1998Before2015,
    USMartinLutherKingJrAfter2015,
    USPresidentsDayBefore2015,
    USPresidentsDayAfter2015,
    GoodFridayBefore2021NotEarlyClose,
    GoodFridayAfter2021,
    GoodFriday2010,
    GoodFriday2012,
    GoodFriday2015,
    GoodFriday2021,
    USMemorialDay2013AndPrior,
    USMemorialDayAfter2013,
    USIndependenceDayBefore2022PreviousDay,
    USIndependenceDayBefore2014,
    USIndependenceDayAfter2014,
    USLaborDayStarting1887Before2014,
    USLaborDayStarting1887After2014,
    USThanksgivingBefore2014,
    USThanksgivingAfter2014,
    USThanksgivingFriday,
)
from pandas_market_calendars.holidays_us import (
    USNewYearsDay,
    ChristmasEveInOrAfter1993,
    Christmas,
    USJuneteenthAfter2022
)

class CMEGlobexEquitiesExchangeCalendar(CMEGlobexBaseExchangeCalendar):

    aliases = ["CME Globex Equity"]

    regular_market_times = {
        "market_open": ((None, time(17), -1),), # offset by -1 day
        "market_close": ((None, time(16)),),
    }

    @property
    def tz(self): return timezone("America/Chicago")

    @property
    def name(self):
        """
        Name of the market

        :return: string name
        """
        return "CME Globex Equities"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFridayBefore2021NotEarlyClose,
            GoodFridayAfter2021,
            Christmas,
        ])

    @property
    def special_closes(self):
        # Source https://www.cmegroup.com/tools-information/holiday-calendar.html
        return [
            (time(10, 30), AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter1998Before2015,
                USPresidentsDayBefore2015,
                USMemorialDay2013AndPrior,
                USIndependenceDayBefore2014,
                USLaborDayStarting1887Before2014,
                USThanksgivingBefore2014,
            ])),

            (time(12,15), AbstractHolidayCalendar(rules= [
                USIndependenceDayBefore2022PreviousDay,
                USThanksgivingFriday,
                ChristmasEveInOrAfter1993,
            ])),

            (time(12), AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter2015,
                USPresidentsDayAfter2015,
                USMemorialDayAfter2013,
                USIndependenceDayAfter2014,
                USLaborDayStarting1887After2014,
                USThanksgivingAfter2014,
                USJuneteenthAfter2022

            ])),
            (time(8,15), AbstractHolidayCalendar(rules=[
                GoodFriday2010,
                GoodFriday2012,
                GoodFriday2015,
                GoodFriday2021,
            ])),

        ]


