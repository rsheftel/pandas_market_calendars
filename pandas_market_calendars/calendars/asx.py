import sys
from datetime import time

import pandas as pd
from pandas.tseries.holiday import AbstractHolidayCalendar, GoodFriday, EasterMonday

# check python versiOn aNd import accordingly
if sys.version_info >= (3, 9):
    # For Python 3.9 and later, import directly
    from zoneinfo import ZoneInfo
else:
    # For Python 3.8 and earlier, import from backports
    from backports.zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.oz import *
from pandas_market_calendars.market_calendar import MarketCalendar


class ASXHolidayCalendar(AbstractHolidayCalendar):
    """
    Custom holiday calendar for ASX with start_date of 2011-01-01.
    This avoids mutating the global AbstractHolidayCalendar.start_date.
    """

    start_date = "2011-01-01"

    def holidays(self, start=None, end=None, return_name=False):
        """
        Override to use self.start_date instead of AbstractHolidayCalendar.start_date.
        This fixes a pandas bug where AbstractHolidayCalendar.holidays() uses the base
        class start_date instead of the subclass/instance start_date.
        """
        if start is None:
            start = self.start_date
        if end is None:
            end = self.end_date
        return super().holidays(start=start, end=end, return_name=return_name)


class ASXExchangeCalendar(MarketCalendar):
    """
    Open Time: 10:00 AM, Australia/Sydney
    Close Time: 4:10 PM, Australia/Sydney

    https://www.asx.com.au/markets/market-resources/trading-hours-calendar/cash-market-trading-hours/trading-calendar

    Regularly-Observed Holidays:
    - New Year's Day (observed on Monday when Jan 1 is a Saturday or Sunday)
    - Australia Day (observed on Monday when Jan 26 is a Saturday or Sunday)
    - Good Friday (two days before Easter Sunday)
    - Easter Monday (the Monday after Easter Sunday)
    - ANZAC Day (April 25)
    - Queen's Birthday (second Monday in June)
    - Christmas Day (December 25, Saturday/Sunday to Monday)
    - Boxing Day (December 26, Saturday to Monday, Sunday to Tuesday)


    Regularly-Observed Early Closes:
    - Last Business Day before Christmas Day
    - Last Business Day of the Year

    """

    aliases = ["ASX"]
    regular_market_times = {
        "market_open": ((None, time(10)),),
        "market_close": ((None, time(16, 10)),),
    }

    @property
    def name(self):
        return "ASX"

    @property
    def full_name(self):
        return "Australian Securities Exchange"

    @property
    def tz(self):
        return ZoneInfo("Australia/Sydney")

    @property
    def regular_holidays(self):
        if not hasattr(self, "_regular_holidays"):
            self._regular_holidays = ASXHolidayCalendar(
                rules=[
                    OZNewYearsDay,
                    AustraliaDay,
                    AnzacDay,
                    QueensBirthday,
                    Christmas,
                    BoxingDay,
                    GoodFriday,
                    EasterMonday,
                ]
            )
        return self._regular_holidays

    @property
    def adhoc_holidays(self):
        return UniqueCloses

    @property
    def special_closes(self):
        if not hasattr(self, "_special_closes"):
            self._special_closes = [
                (
                    time(hour=14, minute=10, tzinfo=self.tz),
                    ASXHolidayCalendar(
                        rules=[
                            ChristmasEve,
                        ]
                    ),
                ),
                (
                    time(hour=14, minute=10, tzinfo=self.tz),
                    ASXHolidayCalendar(
                        rules=[
                            NewYearsEve,
                        ]
                    ),
                ),
            ]
        return self._special_closes
