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

from pandas.tseries.holiday import (
    Holiday,
weekend_to_monday
)
from pytz import timezone

# Useful resources for making changes to this file:
# http://www.cmegroup.com/tools-information/holiday-calendar.html

from .market_calendar import MarketCalendar
from pandas.tseries.holiday import AbstractHolidayCalendar

# New Year's Day
SHFENewYearsDay = Holiday(
    "New Year's Day",
    month=1,
    day=1,
    observance=weekend_to_monday,
)

TombDay2017 = Holiday(
    "Tomb Day 2017",
    month=4,
    day=3
)

TombDay22017 = Holiday(
    "Tomb Day 2017",
    month=4,
    day=4
)

LaborDay2017 = Holiday(
    "Labor Day 2017",
    month=5,
    day=1
)

DragonBoat2017 = Holiday(
    "Dragon Boat 2017",
    month=5,
    day=29
)

DragonBoat22017 = Holiday(
    "Dragon Boat 2017",
    month=5,
    day=30
)

MidAutumn2017 = Holiday(
    "Mid Autumn 2017",
    month=10,
    day=2
)
MidAutumn22017 = Holiday(
    "Mid Autumn 2017",
    month=10,
    day=3
)
MidAutumn32017 = Holiday(
    "Mid Autumn 2017",
    month=10,
    day=4
)
MidAutumn42017 = Holiday(
    "Mid Autumn 2017",
    month=10,
    day=5
)
MidAutumn52017 = Holiday(
    "Mid Autumn 2017",
    month=10,
    day=6
)
class SHFEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for SHFE

    """
    @property
    def name(self):
        return "SHFE"

    @property
    def tz(self):
        return timezone('Asia/Shanghai')

    @property
    def open_time(self):
        return time(9, 1)

    @property
    def close_time(self):
        return time(15)

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            SHFENewYearsDay,
            TombDay2017,
            TombDay2017,
            LaborDay2017,
            DragonBoat2017,
            DragonBoat22017,
            MidAutumn2017,
            MidAutumn22017,
            MidAutumn32017,
            MidAutumn42017,
            MidAutumn52017
        ])