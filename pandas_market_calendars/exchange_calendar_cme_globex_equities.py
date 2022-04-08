from abc import ABC, abstractmethod
from .exchange_calendar_cme_globex_base import CMEGlobexBaseExchangeCalendar

from datetime import time
from itertools import chain

from pandas import Timestamp
from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, USLaborDay, USPresidentsDay, USThanksgivingDay
from pytz import timezone

from pandas_market_calendars.holidays_cme import (
    USMartinLutherKingJrAfter1998Before2015,
    USMartinLutherKingJrAfter2015Before2022,
    USPresidentsDayBefore2015,
    USPresidentsDayAfter2015,
    USPresidentsDayBefore2022,
    GoodFridayBefore2021NotEarlyClose,
    GoodFriday2021,
    GoodFridayAfter2021,
    GoodFriday2010,
    GoodFriday2012,
    GoodFriday2015,
    GoodFriday2021,
    USMemorialDay2021AndPrior,
    USMemorialDay2013AndPrior,
    USMemorialDay2013To2021,
    USIndependenceDayBefore2022,
    USIndependenceDayBefore2022PreviousDay,
    USIndependenceDayBefore2014,
    USIndependenceDayAfter2014,
    USLaborDayStarting1887Before2022,
    USLaborDayStarting1887Before2014,
    USLaborDayStarting1887After2014Before2022,
    USThanksgivingBefore2014,
    USThanksgivingAfter2014Before2022,
    USThanksgivingFriday,
)
from pandas_market_calendars.holidays_us import (
    USNewYearsDay,
    ChristmasEveInOrAfter1993,
    Christmas,
    USJuneteenthAfter2022
)

class CMEGlobexEquitiesExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    """
        * Martin Luther King  --- done
            2014 and before
                10:30 early close on the 3rd Monday of January
            after
                12:00 ''


    """
    """
        * President's Day
            2014 and before
                10:30 early close on the 3rd Monday of February
            after
                12:00 ''
    """
    """
        * Memorial Day
            before
                10:30 early close on the monday

            2013 and after
                12:00 early close on the Monday
    """
    """
        * Juneteenth DONE
            2022
                12:00 early close Monday after
                
    """
    """
        * Independence Day / July 4th
            2009
                10:30 early close on 3rd (Fri)

            2010
                10:30 early close on 5th (Mon)

            2011
                10:30 early close on 4th (Mon)

            2012
                12:15 early close on 3rd (Tue)
                10:30 early close on 4th (Wed)

            2014
                12:15 early close on July 3rd (Thursday)
                12:00 early close on July 4th (Friday)
            2015
                12:00 early close on July 3rd (Friday)                
            2016
                12:00 early close on July 4th (Monday)                
            2017
                12:15 early close on July 3rd (Monday)
                12:00 early close on July 4th (Tuesday)                
            2018
                12:15 early close in 3rd (Tuesday)
                12:00 early close on 4th (Wed)
            2019
                12:15 early close on 3rd (Wed)
                12:00 early close on 4th (Thu)

            2020
                12:00 early close on 3rd (Fri)

            2021
                12:00 early close on 5th (Mon)
                
                
            holiday (july4th) is the nearest workday
                on that day, always early close
            
            if july 4th is Tue-Fri
                then july3rd is special early close
            
            
            
        """
    """
        * Labor Day

            before
                10:30 early close on the monday

            2014 and after
                12:00 early close on the monday
    """
    """
        * Thanksgiving

            before
                10:30 early close on the Thursday
                12:15 early close on the Friday after


            2014 and after
                12:00 early close on the Thursday
                12:15 early close on the Friday after
    """
    """

        * Christmas  --------- GLOBEX  DONE
            --> nearest workday
        
            2009
                1215 on 24th (Thu)
                full close on 25th
            2010
                full close on 24th (Fri) 
            
            2011
                full close on 26th (Mon)
                
            2012
                1215 on 24th (Mon)
                full close on 25th
            
            2014
                
            
                
    """
    """
        * New years ----------- GLOBEX
            
            
            
    """
    """
        * Good Friday  ---------- GLOBEX    DONE
            2009
                fully closed
            2010
                8:15 early close
            2011
                fully closed
            2012
                8:15 early close
            2014
                fully closed
            2015
                8:15 early close on the Friday before easter
            2016 - 2020 (incl)
                fully closed
            2021
                8:15 early close
            2022
                fully closed
            
    """

    regular_market_times = {
        "market_open": ((None, time(17), -1),), # offset by -1 day
        "market_close": ((None, time(16)),),
        "break_start": ((None, time(17)),),
        "break_end": ((None, time(18)),)
    }

    @property
    def tz(self): return timezone("America/Chicago")

    @property
    def name(self):
        """
        Name of the market

        :return: string name
        """
        raise NotImplementedError()

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
                USMartinLutherKingJrAfter2015Before2022,
                USPresidentsDayAfter2015,
                USMemorialDay2013To2021,
                USIndependenceDayAfter2014,
                USLaborDayStarting1887After2014Before2022,
                USThanksgivingAfter2014Before2022,
                USJuneteenthAfter2022

            ])),
            (time(8,15), AbstractHolidayCalendar(rules=[
                GoodFriday2010,
                GoodFriday2012,
                GoodFriday2015,
                GoodFriday2021,
            ])),

        ]


