from .exchange_calendar_cme_globex_base import CMEGlobexBaseExchangeCalendar

from datetime import time
from pandas.tseries.holiday import AbstractHolidayCalendar
from pytz import timezone

from pandas_market_calendars.holidays_cme import (
    USMartinLutherKingJrAfter1998Before2015,
    USMartinLutherKingJrAfter1998Before2016FridayBefore,
    USMartinLutherKingJrAfter2015,
    USPresidentsDayBefore2016FridayBefore,
    USPresidentsDayBefore2015,
    USPresidentsDayAfter2015,
    GoodFridayBefore2021NotEarlyClose,
    GoodFridayAfter2021,
    GoodFriday2009,
    GoodFriday2010,
    GoodFriday2012,
    GoodFriday2015,
    GoodFriday2021,
    USMemorialDay2013AndPrior,
    USMemorialDayAfter2013,
    USMemorialDay2015AndPriorFridayBefore,
    USIndependenceDayBefore2014,
    USIndependenceDayAfter2014,
    USLaborDayStarting1887Before2014,
    USLaborDayStarting1887Before2015FridayBefore,
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


class CMEGlobexFixedIncomeCalendar(CMEGlobexBaseExchangeCalendar):
    aliases = ["CME Globex Fixed Income", "CME Globex Interest Rate Products"]

    regular_market_times = {
        "market_open": ((None, time(18), -1),),
        "market_close": ((None, time(17)),),
    }

    """ 
    Not yet implemented:
        Christmas/New_Years
            5am special open for a couple years (see tests)
        
        regular market_open/market_close changed from 17/16 to 18/17?
    """

    @property
    def name(self): return "CME Globex Fixed Income"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFridayBefore2021NotEarlyClose,
            GoodFridayAfter2021,
            Christmas,
        ])

    @property
    def special_closes_adhoc(self):
        return [(time(15,15), ["2010-07-02", "2011-07-01"]),
                (time(12,15), ["2010-12-31"])]

    @property
    def special_closes(self):
        # Source https://www.cmegroup.com/tools-information/holiday-calendar.html
        return [
            (time(12), AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter1998Before2015,
                USMartinLutherKingJrAfter2015,
                USPresidentsDayBefore2015,
                USPresidentsDayAfter2015,
                USMemorialDay2013AndPrior,
                USMemorialDayAfter2013,
                USIndependenceDayBefore2014,
                USIndependenceDayAfter2014,
                USLaborDayStarting1887Before2014,
                USLaborDayStarting1887After2014,
                USThanksgivingBefore2014,
                USThanksgivingAfter2014,
                USJuneteenthAfter2022,
            ])),

            (time(15,15), AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter1998Before2016FridayBefore,
                USPresidentsDayBefore2016FridayBefore,
                GoodFriday2009,
                USMemorialDay2015AndPriorFridayBefore,
                USLaborDayStarting1887Before2015FridayBefore
            ])),

            (time(12,15), AbstractHolidayCalendar(rules= [
                USThanksgivingFriday,
                ChristmasEveInOrAfter1993,
            ])),

            (time(10,15), AbstractHolidayCalendar(rules=[
                GoodFriday2010,
                GoodFriday2012,
                GoodFriday2015,
                GoodFriday2021,
            ])),

        ]