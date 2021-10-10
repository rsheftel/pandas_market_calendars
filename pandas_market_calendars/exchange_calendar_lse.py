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

from pandas.tseries.holiday import AbstractHolidayCalendar, EasterMonday, GoodFriday
from pytz import timezone

from .holidays_uk import (
    BoxingDay, Christmas, ChristmasEve, LSENewYearsDay, LSENewYearsEve,
    MayBank_pre_1995, MayBank_post_1995_pre_2020, MayBank_post_2020,
    SpringBank_pre_2002, SpringBank_post_2002_pre_2012, SpringBank_post_2012_pre_2022, SpringBank_post_2022,
    SummerBank, WeekendBoxingDay, WeekendChristmas, UniqueCloses,
)
from .market_calendar import MarketCalendar


class LSEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for the London Stock Exchange

    Open Time: 8:00 AM, GMT
    Close Time: 4:30 PM, GMT

    Regularly-Observed Holidays:
    - New Years Day (observed on first business day on/after)
    - Good Friday
    - Easter Monday
    - Early May Bank Holiday (first Monday in May)
    - Spring Bank Holiday (last Monday in May)
    - Summer Bank Holiday (last Monday in August)
    - Christmas Day
    - Dec. 27th (if Christmas is on a weekend)
    - Boxing Day
    - Dec. 28th (if Boxing Day is on a weekend)
    """
    aliases = ['LSE']
    regular_market_times = {
        "market_open": ((None, time(8)),),
        "market_close": ((None, time(16,30)),),

    }

    @property
    def name(self):
        return "LSE"

    @property
    def tz(self):
        return timezone('Europe/London')

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            LSENewYearsDay,
            GoodFriday,
            EasterMonday,
            MayBank_pre_1995, MayBank_post_1995_pre_2020, MayBank_post_2020,
            SpringBank_pre_2002, SpringBank_post_2002_pre_2012, SpringBank_post_2012_pre_2022, SpringBank_post_2022,
            SummerBank,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay
        ])

    @property
    def adhoc_holidays(self):
        return UniqueCloses

    @property
    def special_closes(self):
        return [(
            time(12, 30),
            AbstractHolidayCalendar(rules=[
                ChristmasEve,
                LSENewYearsEve,
            ])
        )]
