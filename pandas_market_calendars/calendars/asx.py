from datetime import time

from pandas.tseries.holiday import AbstractHolidayCalendar, EasterMonday, GoodFriday
from zoneinfo import ZoneInfo

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


# ASX 24 early-close dates: actual Dec 24 and Dec 31 regardless of weekday,
# unlike the cash market which uses previous_friday observance.
_ASX24ChristmasEve = Holiday("Christmas Eve", month=12, day=24)
_ASX24NewYearsEve = Holiday("New Year's Eve", month=12, day=31)


class ASX24FuturesCalendar(MarketCalendar):
    """
    ASX 24 Derivatives Market — Interest Rate & Equity Index Futures
    (XT  — 10 Year Treasury Bond Futures & Options,
     YT  — 3 Year Treasury Bond Futures & Options,
     IR  — 90 Day Bank Bill Futures & Options,
     AP  — SPI 200™ Index Futures & Options)

    ASX 24 is the trading platform for Australian and New Zealand interest
    rate, equity and commodity futures. It operates some of the world's
    longest trading hours via a day + night session structure.

    Sessions (AEST = UTC+10, AEDT = UTC+11 Oct–Apr):
        Day session  : 08:30 – 16:30 AEST/AEDT
        Night session: 17:10 – 08:00 AEST/AEDT (next calendar day)
    Modelled as: open=08:30, break_start=16:30, break_end=17:10,
                 close=08:00+1 (next day offset).

    Early closes (day session only, close 12:00 AEST/AEDT; no night session):
        - Christmas Eve (24 Dec)
        - New Year's Eve (31 Dec)
    Unlike the cash market, these apply to the actual calendar date
    regardless of day of week.

    Holidays: same Australian public holidays as the cash ASX market.
    Night session is also cancelled when the following day is a public
    holiday — this is not modelled (library limitation).

    Source: https://www.asx.com.au/markets/trade-our-derivatives-market/futures-market
    """

    aliases = ["ASX24", "SFE"]

    regular_market_times = {
        "market_open": ((None, time(8, 30)),),
        "market_close": ((None, time(8, 0), 1),),  # 08:00 AEST/AEDT next calendar day
        "break_start": ((None, time(16, 30)),),  # end of day session
        "break_end": ((None, time(17, 10)),),  # start of night session
    }

    @property
    def name(self):
        return "ASX24"

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

    @property
    def special_closes(self):
        return [
            (
                time(12, 0),
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
