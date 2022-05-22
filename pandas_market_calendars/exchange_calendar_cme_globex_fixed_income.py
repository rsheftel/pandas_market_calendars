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


class CMEGlobexFixedIncomeCalendar(CMEGlobexBaseExchangeCalendar):
    regular_market_times = {
        "market_open": ((None, time(18), -1),),
        "market_close": ((None, time(17)),),

        # regular times changed from 17/16 to 18/17?
    }

    """ 
    MLK 
        before 2016, there was a special close on the friday before
        but the mlk day itself always had a halt at 12:00
    
    President's Day
        almost the same as MLK
        
    Good Friday
        Same as equities (also the odd early closes)
        
    Independence Day
        Seems to be same as equities except that the day before independence day special close
        doesn't seem to exist
    
    Labor Day
        
        Mostly the same as equities except that there is an extra early close on the friday before
        the first few years
        
    Thanksgiving
    
        Essentially the same except for the different early close time in the first few years
        
    Christmas
        Essentially the same except for the different early close time in the first few years  <<-- weird 5am for a couple years
           
        
        
    """

    @property
    def name(self): return "CME Fixed Income"


    @property
    def regular_holidays(self):
         return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            Christmas,
        ])

    @property
    def special_closes(self):
        return [(time(15,15), AbstractHolidayCalendar(rules= [

        ]))]