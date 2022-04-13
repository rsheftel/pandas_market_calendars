#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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




class CMEGlobexAgricultureExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    """
    Exchange calendar for CME for Agriculture products

    Products:
    - Grains and Oilseeds (same trading hours and holidays)
    - Livestock
    - Dairy
    - Fertilizer
    - Lumber and Softs


     """

    @property
    @abstractmethod 
    def name(self):
        """
        Name of the market

        :return: string name
        """
        raise NotImplementedError()


class CMEGlobexLivestockExchangeCalendar(CMEGlobexAgricultureExchangeCalendar):
    """
    Exchange calendar for CME for Livestock products

    https://www.cmegroup.com/trading/agricultural/livestock.html

    GLOBEX Trading Times
    https://www.cmegroup.com/markets/agriculture/livestock/live-cattle.contractSpecs.html
    Monday - Friday: 8:30 a.m. - 1:05 p.m. CT
    """
    aliases = ['CMEGlobex_Livestock', 'CMEGlobex_Live_Cattle', 'CMEGlobex_Feeder_Cattle', 'CMEGlobex_Lean_Hog', 'CMEGlobex_Port_Cutout']

    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(13, 5)),)
    }

    @property
    def name(self):
        return "CMEGlobex_Livestock"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            USMartinLutherKingJrAfter1998,
            USPresidentsDay,
            GoodFriday,
            USMemorialDay,
            USIndependenceDay,
            USLaborDay,
            USThanksgivingDay,
            Christmas,
        ])

    # @property
    # def adhoc_holidays(self):
    #     return USNationalDaysofMourning

    @property
    def special_closes(self):
        return [(
            time(12, 5),
            AbstractHolidayCalendar(rules=[
                USBlackFridayInOrAfter1993,
                ChristmasEveBefore1993,
                ChristmasEveInOrAfter1993,
            ])
        )]


