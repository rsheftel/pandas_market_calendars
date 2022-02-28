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

import warnings
from abc import ABC, abstractmethod

from datetime import time
from itertools import chain

from pandas import Timestamp
from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, USLaborDay, USPresidentsDay, USThanksgivingDay
from pytz import timezone

from .holidays_us import (Christmas, ChristmasEveBefore1993, ChristmasEveInOrAfter1993, USBlackFridayInOrAfter1993,
                          USIndependenceDay, USMartinLutherKingJrAfter1998, USMemorialDay, USJuneteenthAfter2022,
                          USNationalDaysofMourning, USNewYearsDay, USThanksgivingFriday)
from .market_calendar import MarketCalendar


class CMEBaseExchangeCalendar(MarketCalendar, ABC):
    """
    Base Exchange Calendar for CME.

    CME Markets: https://www.cmegroup.com/markets/agriculture.html#overview
    - Agriculture
    - Energy
    - Equity Index
    - FX
    - Interest Rates
    - Metals
    - Options

    Holiays for which entire GLOBEX is closed:
    - New Years Day
    - Good Friday
    - Christmas

    Product Specific Closures:
    - MLK Day
    - Presidents Day
    - Memorial Day
    - Juneteenth
    - US Independence Day
    - US Labor Day
    - US Thanksgiving Day
    """
    @property
    @abstractmethod
    def name(self):
        """
        Name of the market

        :return: string name
        """
        raise NotImplementedError()

    @property
    def tz(self):
        return timezone('America/Chicago')

    @property
    def regular_holidays(self):
         return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            Christmas,
        ])

    # I can't find any reference to these special closings onther than NYSE
    # @property
    # def adhoc_holidays(self):
    #     return USNationalDaysofMourning
 
    @property
    def special_closes(self):
        return [(
            self.special_close_time,
            AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                USMemorialDay,
                USJuneteenthAfter2022,
                USLaborDay,
                USIndependenceDay,
                USThanksgivingDay,
                USBlackFridayInOrAfter1993,
                ChristmasEveBefore1993,
                ChristmasEveInOrAfter1993,
            ])
        )]





class CMEAgricultureExchangeCalendar(CMEBaseExchangeCalendar):
    """
    Exchange calendar for CME for Agriculture products

    Products:
    - Grains and Oilseeds (same trading hours and holidays)
    - Livestock
    - Dairy
    - Fertilizer
    - Lumber and Softs


     """
#    aliases = ['CME_Agriculture', 'CBOT_Agriculture', 'COMEX_Agriculture', 'NYMEX_Agriculture']

    @property
    #@abstractmethod  #Would have prefered to keep this class abstract but it fails test_market_calendar.py
    def name(self):
        """
        Name of the market

        :return: string name
        """
        raise NotImplementedError()


class CMELivestockExchangeCalendar(CMEAgricultureExchangeCalendar):
    """
    Exchange calendar for CME for Livestock products

    https://www.cmegroup.com/trading/agricultural/livestock.html

    GLOBEX Trading Times
    https://www.cmegroup.com/markets/agriculture/livestock/live-cattle.contractSpecs.html
    Monday - Friday: 8:30 a.m. - 1:05 p.m. CT
    """
    aliases = ['CME_Livestock', 'CME_Live_Cattle', 'CME_Feeder_Cattle', 'CME_Lean_Hog', 'CME_Port_Cutout']

    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(13, 5)),)
    }

    @property
    def name(self):
        return "CME_Livestock"

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



class CMEEquityExchangeCalendar(CMEBaseExchangeCalendar):
    aliases = ['CME_Equity', 'CBOT_Equity', '/ES', 'S&P500']

    # Using CME Globex trading times
    # https://www.cmegroup.com/markets/equities/sp/e-mini-sandp500.contractSpecs.html
    regular_market_times = {
        "market_open": ((None, time(17), -1),), # offset by -1 day
        "market_close": ((None, time(16, 00)),)
        #"break_start": ((None, time(17,45)),),
        #"break_end": ((None, time(17,30)),)
    }

    @property
    def name(self):
        return "CME_Equity"

    @property
    def special_close_time(self):
        return time(12, 30)




# For the bond market Good Friday that coincides with the release of NFP on the first friday of the month is an open day
goodFridayClosed = ['1970-03-27', '1971-04-09', '1972-03-31', '1973-04-20', '1974-04-12', '1975-03-28', '1976-04-16',
                    '1977-04-08', '1978-03-24', '1979-04-13', '1981-04-17', '1982-04-09', '1984-04-20', '1986-03-28',
                    '1987-04-17', '1989-03-24', '1990-04-13', '1991-03-29', '1992-04-17', '1993-04-09', '1995-04-14',
                    '1997-03-28', '1998-04-10', '2000-04-21', '2001-04-13', '2002-03-29', '2003-04-18', '2004-04-09',
                    '2005-03-25', '2006-04-14', '2008-03-21', '2009-04-10', '2011-04-22', '2013-03-29', '2014-04-18',
                    '2016-03-25', '2017-04-14', '2018-03-30', '2019-04-19', '2020-04-10', '2022-04-15', '2024-03-29',
                    '2025-04-18', '2027-03-26', '2028-04-14', '2029-03-30', '2030-04-19', '2031-04-11', '2032-03-26',
                    '2033-04-15', '2035-03-23', '2036-04-11', '2038-04-23', '2039-04-08', '2040-03-30', '2041-04-19',
                    '2043-03-27', '2044-04-15', '2046-03-23', '2047-04-12', '2049-04-16', '2050-04-08', '2051-03-31',
                    '2052-04-19', '2054-03-27', '2055-04-16', '2056-03-31', '2057-04-20', '2058-04-12', '2059-03-28',
                    '2060-04-16', '2061-04-08', '2062-03-24', '2063-04-13', '2065-03-27', '2066-04-09', '2068-04-20',
                    '2069-04-12', '2070-03-28', '2071-04-17', '2072-04-08', '2073-03-24', '2074-04-13', '2076-04-17',
                    '2077-04-09', '2079-04-21', '2081-03-28', '2082-04-17', '2084-03-24', '2085-04-13', '2086-03-29',
                    '2087-04-18', '2088-04-09', '2090-04-14', '2092-03-28', '2093-04-10', '2095-04-22', '2096-04-13',
                    '2097-03-29', '2098-04-18', '2099-04-10']

BondsGoodFridayClosed = [Timestamp(x, tz='UTC') for x in goodFridayClosed]

goodFridayOpen = ['1980-04-04', '1983-04-01', '1985-04-05', '1988-04-01', '1994-04-01', '1996-04-05', '1999-04-02',
                  '2007-04-06', '2010-04-02', '2012-04-06', '2015-04-03', '2021-04-02', '2023-04-07', '2026-04-03',
                  '2034-04-07', '2037-04-03', '2042-04-04', '2045-04-07', '2048-04-03', '2053-04-04', '2064-04-04',
                  '2067-04-01', '2075-04-05', '2078-04-01', '2080-04-05', '2083-04-02', '2089-04-01', '2091-04-06',
                  '2094-04-02']

BondsGoodFridayOpen = [Timestamp(x, tz='UTC') for x in goodFridayOpen]


class CMEBondExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for CME for Interest Rate and Bond products

    The Holiday calendar is different between the open outcry trading floor hours and GLOBEX electronic trading hours.
    This calendar attempts to be accurate for the GLOBEX holidays and hours from approx 2010 onward.
    """
    aliases = ['CME_Rate', 'CBOT_Rate', 'CME_InterestRate', 'CBOT_InterestRate', 'CME_Bond', 'CBOT_Bond']
    regular_market_times = {
        "market_open": ((None, time(17), -1),), # offset by -1 day
        "market_close": ((None, time(16)),)
    }

    @property
    def name(self):
        return "CME_Bond"

    @property
    def tz(self):
        return timezone('America/Chicago')

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            Christmas,
        ])

    @property
    def adhoc_holidays(self):
        return list(chain(USNationalDaysofMourning, BondsGoodFridayClosed))

    @property
    def special_closes(self):
        return [
            (time(12),
             AbstractHolidayCalendar(rules=[
                 USMartinLutherKingJrAfter1998,
                 USPresidentsDay,
                 USMemorialDay,
                 USIndependenceDay,
                 USLaborDay,
                 USThanksgivingDay,
             ])),
            (time(12, 15),
             AbstractHolidayCalendar(rules=[
                 USBlackFridayInOrAfter1993,
                 ChristmasEveBefore1993,
                 ChristmasEveInOrAfter1993,
             ]))
        ]

    @property
    def special_closes_adhoc(self):
        return [
            (time(10, tzinfo=self.tz), BondsGoodFridayOpen)
        ]


class CMECurrencyExchangeCalendar(CMEBaseExchangeCalendar):
    aliases = ['CME_Currency']

    # Using CME Globex trading times eg AUD/USD, EUR/GBP, and BRL/USD
    # https://www.cmegroup.com/markets/fx/g10/australian-dollar.contractSpecs.html
    # https://www.cmegroup.com/markets/fx/cross-rates/euro-fx-british-pound.contractSpecs.html
    # https://www.cmegroup.com/markets/fx/emerging-market/brazilian-real.contractSpecs.html
    # CME "NZD spot" has its own holiday schedule; this is a niche product (via "FX Link") and is not handled in this
    # class; however, its regular hours follow the same schedule (see
    # https://www.cmegroup.com/trading/fx/files/fx-product-guide-2021-us.pdf)
    regular_market_times = {
        "market_open": ((None, time(17), -1),),  # offset by -1 day
        "market_close": ((None, time(16, 00)),)
    }

    @property
    def name(self):
        return "CME_Currency"

    @property
    def special_close_time(self):
        return time(12, 15)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            Christmas,
        ])

    @property
    def special_closes(self):
        # Currency futures are typically fully closed or they trade normal hours; Thanksgiving Friday is the exception
        return [(
            self.special_close_time,
            AbstractHolidayCalendar(rules=[
                USThanksgivingFriday,
            ])
        )]
