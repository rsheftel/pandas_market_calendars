import datetime as dt

import pytz
from pandas.tseries.holiday import AbstractHolidayCalendar

from pandas_market_calendars.holidays.cme import (
    GoodFriday2021,
    GoodFriday2022,
    GoodFridayAfter2022,
    GoodFridayBefore2021,
    USIndependenceDayBefore2022PreviousDay,
)
from pandas_market_calendars.holidays.cme_globex import (
    ChristmasCME,
    USMartinLutherKingJrFrom2022,
    USMartinLutherKingJrPre2022,
    USPresidentsDayFrom2022,
    USPresidentsDayPre2022,
    USMemorialDayFrom2022,
    USMemorialDayPre2022,
    USJuneteenthFrom2022,
    USIndependenceDayFrom2022,
    USIndependenceDayPre2022,
    USLaborDayFrom2022,
    USLaborDayPre2022,
    USThanksgivingDayFrom2022,
    USThanksgivingDayPre2022,
    USThanksgivingFridayFrom2021,
    USThanksgivingFridayPre2021,
)
from pandas_market_calendars.holidays.us import (
    ChristmasEveInOrAfter1993,
    USNewYearsDay,
)
from .cme_globex_base import CMEGlobexBaseExchangeCalendar


# https://github.com/rsheftel/pandas_market_calendars/blob/master/docs/new_market.rst
class CMEGlobexCryptoExchangeCalendar(CMEGlobexBaseExchangeCalendar):
    # The label you fetch the exchange with in mcal.get_calendar('CME Globex ...')
    aliases = ["CME Globex Cryptocurrencies", "CME Globex Crypto"]

    # https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/bitcoin.contractSpecs.html
    regular_market_times = {
        # Tuple[Tuple[first date used, time, offset], ...]
        # -1 offset indicates that the open is on the previous day
        # None for first date used marks the start, subsequent market times must have an actual timestamp
        "market_open": (
            (None, dt.time(17, tzinfo=pytz.timezone("America/Chicago")), -1),
        ),
        "market_close": (
            (
                None,
                dt.time(16, tzinfo=pytz.timezone("America/Chicago")),
            ),
        ),
        "break_start": (
            (
                None,
                dt.time(16, tzinfo=pytz.timezone("America/Chicago")),
            ),
        ),
        "break_end": (
            (
                None,
                dt.time(17, tzinfo=pytz.timezone("America/Chicago")),
            ),
        ),
    }

    @property
    def tz(self):
        # Central Time
        return pytz.timezone("America/Chicago")

    @property
    def name(self):
        return "CME Globex Crypto"

    # Check the .zip files at the bottom of this page
    # https://www.cmegroup.com/tools-information/holiday-calendar.html?redirect=/tools-information/holiday-calendar/#cmeGlobex
    # Note: many of the holiday objects (ie. GoodFridayBefore2021) were originally made for equities and other markets
    #   and hence have a start_date starting before crypto is actually available

    @property
    def regular_holidays(self):
        # Days where the market is fully closed
        return AbstractHolidayCalendar(
            rules=[
                GoodFridayBefore2021,
                GoodFriday2022,
                ChristmasCME,
                USNewYearsDay,
            ]
        )

    @property
    def special_closes(self):
        # Days where the market closes early
        # list[Tuple[time, AbstractHolidayCalendar]]
        return [
            (
                dt.time(8, 15, tzinfo=pytz.timezone("America/Chicago")),
                AbstractHolidayCalendar(
                    rules=[
                        GoodFriday2021,
                    ]
                ),
            ),
            (
                dt.time(10, 15, tzinfo=pytz.timezone("America/Chicago")),
                AbstractHolidayCalendar(
                    rules=[
                        GoodFridayAfter2022,
                    ]
                ),
            ),
            (
                dt.time(12, tzinfo=pytz.timezone("America/Chicago")),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrPre2022,
                        USPresidentsDayPre2022,
                        USMemorialDayPre2022,
                        USIndependenceDayPre2022,
                        USLaborDayPre2022,
                        USThanksgivingDayPre2022,
                    ]
                ),
            ),
            (
                dt.time(12, 15, tzinfo=pytz.timezone("America/Chicago")),
                AbstractHolidayCalendar(
                    rules=[
                        ChristmasEveInOrAfter1993,
                        USIndependenceDayBefore2022PreviousDay,
                        USThanksgivingFridayPre2021,
                    ]
                ),
            ),
            (
                dt.time(12, 45, tzinfo=pytz.timezone("America/Chicago")),
                AbstractHolidayCalendar(rules=[USThanksgivingFridayFrom2021]),
            ),
            # TODO: this market already closes at 1600 normally, do we need these holidays?
            (
                dt.time(16, tzinfo=pytz.timezone("America/Chicago")),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrFrom2022,
                        USPresidentsDayFrom2022,
                        USMemorialDayFrom2022,
                        USJuneteenthFrom2022,
                        USIndependenceDayFrom2022,
                        USLaborDayFrom2022,
                        USThanksgivingDayFrom2022,
                    ]
                ),
            ),
        ]
