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

from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
)
from pytz import timezone

from pandas_market_calendars.holidays.us import (
    Christmas,
    ChristmasEveBefore1993,
    ChristmasEveInOrAfter1993,
    USBlackFridayInOrAfter1993,
    USIndependenceDay,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USJuneteenthAfter2022,
    USNewYearsDay,
)
from pandas_market_calendars.market_calendar import MarketCalendar


class CMEGlobexBaseExchangeCalendar(MarketCalendar, ABC):
    """
    Base Exchange Calendar for CME.

    CME Markets: https://www.cmegroup.com/markets/agriculture.html#overview
    - Agriculture
    - Crypto
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
        return timezone("America/Chicago")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                GoodFriday,
                Christmas,
            ]
        )

    # I can't find any reference to these special closings onther than NYSE
    # @property
    # def adhoc_holidays(self):
    #     return USNationalDaysofMourning

    @property
    def special_closes(self):
        return [
            (
                self.special_close_time,
                AbstractHolidayCalendar(
                    rules=[
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
                    ]
                ),
            )
        ]
