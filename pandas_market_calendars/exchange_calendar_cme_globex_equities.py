from abc import ABC, abstractmethod
from .exchange_calendar_cme_globex_base import CMEGlobexBaseExchangeCalendar

from datetime import time
from itertools import chain

from pandas import Timestamp
from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, USLaborDay, USPresidentsDay, USThanksgivingDay
from pytz import timezone

from .holidays_us import (Christmas, ChristmasEveBefore1993, ChristmasEveInOrAfter1993, USBlackFridayInOrAfter1993,
                          USIndependenceDay, USMartinLutherKingJrAfter1998, USMemorialDay, USJuneteenthAfter2022,
                          USNationalDaysofMourning, USNewYearsDay)
from .market_calendar import MarketCalendar


class CMEGlobexEquitiesExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    """
    Holidays overview

        * Martin Luther King
            2014 and before
                10:30 early close on the 3rd Monday of January
            after
                12:00 ''

        * President's Day
            2014 and before
                10:30 early close on the 3rd Monday of February
            after
                12:00 ''

        * Good Friday
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

        * Memorial Day
            before
                10:30 early close on the monday

            2014 and after
                12:00 early close on the Monday

        * Juneteenth
            2022
                12:00 early close Monday after

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

        * Labor Day

            before
                10:30 early close on the monday

            2014 and after
                12:00 early close on the monday

        * Thanksgiving

            before
                10:30 early close on the Thursday
                12:15 early close on the Friday after


            2014 and after
                12:00 early close on the Thursday
                12:15 early close on the Friday after


        * Christmas

                pretty weird check later

        * New years
                also pretty weird



























    """


    @property
    @abstractmethod
    def name(self):
        """
        Name of the market

        :return: string name
        """
        raise NotImplementedError()














