import sys
from datetime import time

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

AbstractHolidayCalendar.start_date = "2011-01-01"


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
        return AbstractHolidayCalendar(
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

    @property
    def adhoc_holidays(self):
        return UniqueCloses

    @property
    def special_closes(self):
        return [
            (
                time(hour=14, minute=10, tzinfo=self.tz),
                AbstractHolidayCalendar(
                    rules=[
                        ChristmasEve,
                    ]
                ),
            ),
            (
                time(hour=14, minute=10, tzinfo=self.tz),
                AbstractHolidayCalendar(
                    rules=[
                        NewYearsEve,
                    ]
                ),
            ),
        ]
