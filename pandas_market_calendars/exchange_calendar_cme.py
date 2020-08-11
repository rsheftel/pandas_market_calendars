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

from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, USLaborDay, USPresidentsDay, USThanksgivingDay
from pytz import timezone

from .exchange_calendar_nyse import NYSEExchangeCalendar
from .holidays_us import (Christmas, ChristmasEveBefore1993, ChristmasEveInOrAfter1993, USBlackFridayInOrAfter1993,
                          USIndependenceDay, USMartinLutherKingJrAfter1998, USMemorialDay, USNationalDaysofMourning,
                          USNewYearsDay)
from .market_calendar import MarketCalendar


# Useful resources for making changes to this file:
# http://www.cmegroup.com/tools-information/holiday-calendar.html


class CMEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for CME

    Open Time: 5:00 PM, America/Chicago
    Close Time: 5:00 PM, America/Chicago

    Regularly-Observed Holidays:
    - New Years Day
    - Good Friday
    - Christmas
    """
    aliases = ['CME', 'CBOT', 'COMEX', 'NYMEX']

    @property
    def name(self):
        return "CME"

    @property
    def tz(self):
        return timezone('America/Chicago')

    @property
    def open_time_default(self):
        return time(17, 1, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(17, tzinfo=self.tz)

    @property
    def open_offset(self):
        return -1

    @property
    def regular_holidays(self):
        # The CME has different holiday rules depending on the type of
        # instrument. For example, http://www.cmegroup.com/tools-information/holiday-calendar/files/2016-4th-of-july-holiday-schedule.pdf # noqa
        # shows that Equity, Interest Rate, FX, Energy, Metals & DME Products
        # close at 1200 CT on July 4, 2016, while Grain, Oilseed & MGEX
        # Products and Livestock, Dairy & Lumber products are completely
        # closed.

        # For now, we will treat the CME as having a single calendar, and just
        # go with the most conservative hours - and treat July 4 as an early
        # close at noon.
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            Christmas,
        ])

    @property
    def adhoc_holidays(self):
        return USNationalDaysofMourning

    @property
    def special_closes(self):
        return [(
            time(12),
            AbstractHolidayCalendar(rules=[
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                USMemorialDay,
                USLaborDay,
                USIndependenceDay,
                USThanksgivingDay,
                USBlackFridayInOrAfter1993,
                ChristmasEveBefore1993,
                ChristmasEveInOrAfter1993,
            ])
        )]


class CMEEquityExchangeCalendar(NYSEExchangeCalendar):
    """
    Exchange calendar for CME for Equity products

    Open Time: 6:00 PM, America/New_York
    Close Time: 5:00 PM, America/New_York
    Break: 4:15 - 4:30pm America/New_York

    Regularly-Observed Holidays same as NYSE equity markets
    """
    aliases = ['CME_Equity', 'CBOT_Equity']

    @property
    def name(self):
        return "CME_Equity"

    @property
    def tz(self):
        return timezone('America/New_York')

    @property
    def open_time_default(self):
        return time(18, 0, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(17, 0, tzinfo=self.tz)

    @property
    def open_offset(self):
        return -1

    @property
    def break_start(self):
        return time(16, 15)

    @property
    def break_end(self):
        return time(16, 30)


class CMEAgricultureExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for CME for Agriculture products

    Open Time: 5:00 PM, America/Chicago
    Close Time: 5:00 PM, America/Chicago

    Regularly-Observed Holidays:
    - New Years Day
    - Good Friday
    - Christmas
    """
    aliases = ['CME_Agriculture', 'CBOT_Agriculture', 'COMEX_Agriculture', 'NYMEX_Agriculture']

    @property
    def name(self):
        return "CME_Agriculture"

    @property
    def tz(self):
        return timezone('America/Chicago')

    @property
    def open_time_default(self):
        return time(17, 1, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(17, tzinfo=self.tz)

    @property
    def open_offset(self):
        return -1

    @property
    def regular_holidays(self):
        # Ignore gap between 13:20 CST and 14:30 CST for regular trading hours
        #
        # The CME has different holiday rules depending on the type of
        # instrument. For example, http://www.cmegroup.com/tools-information/holiday-calendar/files/2016-4th-of-july-holiday-schedule.pdf # noqa
        # shows that Equity, Interest Rate, FX, Energy, Metals & DME Products
        # close at 1200 CT on July 4, 2016, while Grain, Oilseed & MGEX
        # Products and Livestock, Dairy & Lumber products are completely
        # closed.
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

    @property
    def adhoc_holidays(self):
        return USNationalDaysofMourning

    @property
    def special_closes(self):
        return [(
            time(12),
            AbstractHolidayCalendar(rules=[
                USBlackFridayInOrAfter1993,
                ChristmasEveBefore1993,
                ChristmasEveInOrAfter1993,
            ])
        )]


class CMEBondExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for CME for Interest Rate and Bond products

    The Holiday calendar is different between the open outcry trading floor hours and GLOBEX electronic trading hours.
    This calendar attempts to be accurate for the GLOBEX holidays and hours from approx 2010 onward.
    """
    aliases = ['CME_Rate', 'CBOT_Rate', 'CME_InterestRate', 'CBOT_InterestRate', 'CME_Bond', 'CBOT_Bond']

    @property
    def name(self):
        return "CME_Bond"

    @property
    def tz(self):
        return timezone('America/Chicago')

    @property
    def open_time_default(self):
        return time(17, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(16, tzinfo=self.tz)

    @property
    def open_offset(self):
        return -1

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            USNewYearsDay,
            GoodFriday,
            Christmas,
        ])

    @property
    def adhoc_holidays(self):
        return USNationalDaysofMourning

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
