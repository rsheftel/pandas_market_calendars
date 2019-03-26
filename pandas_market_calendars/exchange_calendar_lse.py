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
from pytz import timezone
from itertools import chain
from pandas.tseries.holiday import AbstractHolidayCalendar
from .market_calendar import (
    MarketCalendar
)

from pandas.tseries.holiday import (
    GoodFriday,
    EasterMonday,
)
from pandas_market_calendars.holidays_uk import (
    LSENewYearsEve,
    LSENewYearsDay,
    MayBank,
    SpringBank,
    SummerBank,
    ChristmasEve,
    Christmas,
    WeekendChristmas,
    BoxingDay,
    WeekendBoxingDay,
    BankHoliday,
    QueensJubilee
)


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

    @property
    def name(self):
        return "LSE"

    @property
    def tz(self):
        return timezone('Europe/London')

    @property
    def open_time_default(self):
        return time(8, 0, tzinfo=self.tz)

    @property
    def close_time_default(self):
        return time(16, 30, tzinfo=self.tz)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            LSENewYearsDay,
            GoodFriday,
            EasterMonday,
            MayBank,
            SpringBank,
            SummerBank,
            Christmas,
            WeekendChristmas,
            BoxingDay,
            WeekendBoxingDay
        ])

    @property
    def adhoc_holidays(self):
        return list(chain(
            BankHoliday,
            QueensJubilee,
        ))

    @property
    def special_closes(self):
        return [(
            time(12, 30),
            AbstractHolidayCalendar(rules=[
                ChristmasEve,
                LSENewYearsEve,
            ])
        )]
