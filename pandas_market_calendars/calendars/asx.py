from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, EasterMonday, GoodFriday
from zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.oz import *
from pandas_market_calendars.market_calendar import HolidayCalendar, MarketCalendar


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
    - Queen's Birthday (second Monday in June) (Now King)
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
        return HolidayCalendar(
            start_date="2011-01-01",
            rules=[
                OZNewYearsDay,
                AustraliaDay,
                AnzacDay,
                QueensBirthday,
                Christmas,
                BoxingDay,
                GoodFriday,
                EasterMonday,
            ],
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


# ASX 24 early-close dates: actual Dec 24 and Dec 31 regardless of weekday,
# unlike the cash market which uses previous_friday observance.
_ASX24ChristmasEve = Holiday("Christmas Eve", month=12, day=24)
_ASX24NewYearsEve = Holiday("New Year's Eve", month=12, day=31)


class ASX24BaseCalendar(MarketCalendar):
    @property
    def tz(self):
        return ZoneInfo("Australia/Sydney")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                OZNewYearsDay,
                AustraliaDay,
                GoodFriday,
                EasterMonday,
                AnzacDay,
                QueensBirthday,
                Christmas,
                BoxingDay,
            ]
        )

    @property
    def adhoc_holidays(self):
        return UniqueCloses

    _early_close_time = None

    @property
    def special_closes(self):
        return [
            (
                self._early_close_time,
                AbstractHolidayCalendar(
                    rules=[
                        _ASX24ChristmasEve,
                        _ASX24NewYearsEve,
                    ]
                ),
            ),
        ]

    @property
    def special_closes_adhoc(self):
        return []


class ASX24IndexFuturesCalendar(ASX24BaseCalendar):
    """
    ASX 24 Derivatives Market — Equity Index Futures
    (AP  — SPI 200™ Index Futures & Options)

    Source: https://www.asx.com.au/markets/market-resources/trading-hours-calendar/
    """

    aliases = ["ASX24_Index", "SFE_Index"]
    _early_close_time = time(14, 30)

    regular_market_times = {
        "market_open": ((None, time(9, 50)),),
        "market_close": ((None, time(8, 0), 1),),  # 08:00 AEST/AEDT next calendar day
        "break_start": ((None, time(16, 30)),),  # end of day session
        "break_end": ((None, time(17, 10)),),  # start of night session
    }

    @property
    def name(self):
        return "ASX24_Index"


class ASX24IRFuturesCalendar(ASX24BaseCalendar):
    """
    ASX 24 Derivatives Market — Interest Rate Futures
    (XT  — 10 Year Treasury Bond Futures & Options,
     YT  — 3 Year Treasury Bond Futures & Options,
     IR  — 90 Day Bank Bill Futures & Options)

     Markets open staggered between 08:28 and 08:34, we have picked the earliest here.

    Source: https://www.asx.com.au/markets/market-resources/trading-hours-calendar/
    """

    aliases = ["ASX24_Rates", "SFE_Rates"]
    _early_close_time = time(12, 30)

    regular_market_times = {
        "market_open": ((None, time(8, 28)),),
        "market_close": ((None, time(7, 0), 1),),  # 08:00 AEST/AEDT next calendar day
        "break_start": ((None, time(16, 30)),),  # end of day session
        "break_end": ((None, time(17, 10)),),  # start of night session
    }

    @property
    def name(self):
        return "ASX24_Rates"
