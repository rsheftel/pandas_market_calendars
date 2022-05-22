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

import pandas as pd
from pandas import Timestamp
from pandas.tseries.holiday import AbstractHolidayCalendar #, GoodFriday, USLaborDay, USPresidentsDay, USThanksgivingDay
from pytz import timezone

#from .holidays_us import (Christmas, ChristmasEveBefore1993, ChristmasEveInOrAfter1993, USBlackFridayInOrAfter1993,
#                          USIndependenceDay, USMartinLutherKingJrAfter1998, USMemorialDay, USJuneteenthAfter2022,
#                          USNationalDaysofMourning, USNewYearsDay)

from .holidays_cme_globex import (  USNewYearsDay,
                                    USMartinLutherKingJrFrom2022, USMartinLutherKingJrPre2022, USNewYearsDay,
                                    USPresidentsDayFrom2022, USPresidentsDayPre2022, 
                                    GoodFriday, 
                                    USMemorialDayFrom2022, USMemorialDayPre2022, 
                                    USJuneteenthFrom2022, 
                                    USIndependenceDayFrom2022, USIndependenceDayPre2022, 
                                    USLaborDay,
                                    USThanksgivingDayFrom2022, USThanksgivingDayPre2022, FridayAfterThanksgiving,
                                    ChristmasCME)                          
from .market_calendar import MarketCalendar




class CMEGlobexEnergyAndMetalsExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    """
    Exchange calendar for CME for Energy and Metals products

    Both follow the same trading/holiday schedule

    NOT IMPLEMENTED: Dubai Mercantile Exchange (DME) follows this schedule but with holiday exceptions.

    Energy Products:
      Crude and Refined: https://www.cmegroup.com/trading/energy/crude-and-refined-products.html 
      - HO NY Harbor ULSD Futures
      - CL Crude Oil Futures
      - RB RBOB Gasoline Futures
      - MCL Micro WTI Crude Oil Futures
      Natural Gas
      - NG Henry Hub Natural Gas Futures
      - TTF Dutch TTF Natural Gas Calendar Month Futures
      - NN Henry Hub Natural Gas Last Day Financial Futures
      Voluntary Carbon Emissions Offset Futures
      - CGO CBL Core Global Emmissions Offset (C-GEO) Futures
      - NGO CBL Nature-based Global Emissionns Offset Futures
      - GEO CBL Global Emissions Offset Futures

    Metals Products: https://www.cmegroup.com/markets/metals.html 
      Precious Metals
      - GC Gold Futures
      - SI Silver Futures
      - PL Platinum Futures
      Base Metals
      - HG Copper Futures
      - ALI Aluminum Futures
      - QC E-mini Copper Futures
      Ferrous Metals
      - HRC U.S. Midwest Domestic Hot-Rolled Coil Steel (CRU) Index Futures
      - BUS U.S. Midwest Busheling Ferrous Scrap (AMM) Futures
      - TIO Iron Ore 62% Fe, CFR China (Platts) Futures

      Sample GLOBEX Trading Times
      https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.contractSpecs.html
      Sunday - Friday: 5:00pm - 4:00 pm CT 

      Calendar: http://www.cmegroup.com/tools-information/holiday-calendar.html
     """

    aliases = [ 'CMEGlobex_EnergyAndMetals',
                'CMEGlobex_Energy',
                   'CMEGlobex_CrudeAndRefined', 'CMEGlobex_NYHarbor', 'CMEGlobex_HO', 'HO', 'CMEGlobex_Crude', 'CMEGlobex_CL', 'CL', 'CMEGlobex_Gas', 'CMEGlobex_RB', 'RB', 'CMEGlobex_MicroCrude', 'CMEGlobex_MCL', 'MCL',
                   'CMEGlobex_NatGas',          'CMEGlobex_NG', 'NG', 'CMEGlobex_Dutch_NatGas', 'CMEGlobex_TTF', 'TTF', 'CMEGlobex_LastDay_NatGas', 'CMEGlobex_NN', 'NN',
                   'CMEGlobex_CarbonOffset',     'CMEGlobex_CGO', 'CGO', 'C-GEO', 'CMEGlobex_NGO', 'NGO', 'CMEGlobex_GEO', 'GEO',
                'CMEGlobex_Metals',
                    'CMEGlobex_PreciousMetals', 'CMEGlobex_Gold', 'CMEGlobex_GC', 'GC', 'CMEGlobex_Silver' 'CMEGlobex_SI', 'SI', 'CMEGlobex_Platinum', 'CMEGlobex_PL', 'PL',
                    'CMEGlobex_BaseMetals',     'CMEGlobex_Copper', 'CMEGlobex_HG', 'HG', 'CMEGlobex_Aluminum', 'CMEGlobex_ALI', 'ALI', 'CMEGlobex_Copper', 'CMEGlobex_QC', 'QC',
                    'CMEGlobex_FerrousMetals',  'CMEGlobex_HRC', 'HRC', 'CMEGlobex_BUS', 'BUS', 'CMEGlobex_TIO', 'TIO' ]

    regular_market_times = {
        "market_open": ((None, time(17), -1),), #Sunday offset. Central Timezone (CT)
        "market_close": ((None, time(16)),)
    }

    @property
    def name(self):
        return "CMEGlobex_EnergyAndMetals"


    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            ChristmasCME,            
         ])

    # @property
    # def adhoc_holidays(self):
    #     return USNationalDaysofMourning

    @property
    def special_closes(self):
        return [
            (time(12, tzinfo=timezone('America/Chicago')), AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrPre2022,
                USPresidentsDayPre2022,
                USMemorialDayPre2022,
                USIndependenceDayPre2022,
                USLaborDay,
                USThanksgivingDayPre2022,
             ])),           
            (time(12, 45, tzinfo=timezone('America/Chicago')), AbstractHolidayCalendar(rules=[
                 FridayAfterThanksgiving,
             ])),           
             (time(13, 30, tzinfo=timezone('America/Chicago')), AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrFrom2022,
                USPresidentsDayFrom2022,
                USMemorialDayFrom2022,
                USJuneteenthFrom2022,
                USIndependenceDayFrom2022,
                USThanksgivingDayFrom2022,
             ])),
         ]


