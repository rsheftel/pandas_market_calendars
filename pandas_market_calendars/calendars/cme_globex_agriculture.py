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
from abc import abstractmethod
from datetime import time
from typing import Any, List

from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
)

from pandas_market_calendars.calendars.cme_market_times import GRAINS_AND_OILSEEDS_MARKET_TIMES
from pandas_market_calendars.holidays.us import (
    Christmas,
    ChristmasEveBefore1993,
    ChristmasEveInOrAfter1993,
    USBlackFridayInOrAfter1993,
    USIndependenceDay,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNewYearsDay,
)

from .cme_globex_base import CMEGlobexBaseExchangeCalendar


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
    def name(self) -> str:
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

    aliases = [
        "CMEGlobex_Livestock",
        "CMEGlobex_Live_Cattle",
        "CMEGlobex_Feeder_Cattle",
        "CMEGlobex_Lean_Hog",
        "CMEGlobex_Port_Cutout",
    ]

    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(13, 5)),),
    }

    @property
    def name(self) -> str:
        return "CMEGlobex_Livestock"

    @property
    def regular_holidays(self) -> Any:
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                GoodFriday,
                USMemorialDay,
                USIndependenceDay,
                USLaborDay,
                USThanksgivingDay,
                Christmas,
            ]
        )

    # @property
    # def adhoc_holidays(self) -> List[Any]:
    #     return USNationalDaysofMourning

    @property
    def special_closes(self) -> List[Any]:
        return [
            (
                time(12, 5),
                AbstractHolidayCalendar(
                    rules=[
                        USBlackFridayInOrAfter1993,
                        ChristmasEveBefore1993,
                        ChristmasEveInOrAfter1993,
                    ]
                ),
            )
        ]


class CMEGlobexGrainsAndOilseedsExchangeCalendar(CMEGlobexAgricultureExchangeCalendar):
    """
    Exchange calendar for CME for Grains & Oilseeds

    https://www.cmegroup.com/trading/agricultural/grain-and-oilseed.html

    GLOBEX Trading Times
    https://www.cmegroup.com/markets/agriculture/oilseeds/soybean.contractSpecs.html
    https://www.cmegroup.com/markets/agriculture/grains/corn.contractSpecs.html
    https://www.cmegroup.com/markets/agriculture/grains/wheat.contractSpecs.html
    Sunday - Friday: 7:00 p.m. - 7:45 a.m. CT and Monday - Friday: 8:30 a.m. - 1:20 p.m. CT
    """

    aliases = [
        "CMEGlobex_Grains",
        "CMEGlobex_Oilseeds",
    ]

    regular_market_times = GRAINS_AND_OILSEEDS_MARKET_TIMES

    @property
    def name(self) -> str:
        return "CMEGlobex_GrainsAndOilseeds"

    @property
    def regular_holidays(self) -> Any:
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                GoodFriday,
                USMemorialDay,
                USIndependenceDay,
                USLaborDay,
                USThanksgivingDay,
                Christmas,
            ]
        )
