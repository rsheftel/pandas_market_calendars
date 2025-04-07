from datetime import time
from itertools import chain

from pandas import Timestamp, DatetimeIndex, Timedelta
from pandas.tseries.holiday import AbstractHolidayCalendar
from zoneinfo import ZoneInfo

from typing import Literal, Union
from pandas_market_calendars import calendar_utils as u

from pandas_market_calendars.holidays.nyse import (
    USPresidentsDay,
    GoodFriday,
    USMemorialDay,
    USJuneteenthAfter2022,
    USIndependenceDay,
    USThanksgivingDay,
    ChristmasNYSE,
    USMartinLutherKingJrAfter1998,
    # Ad-Hoc
    DayAfterThanksgiving1pmEarlyCloseInOrAfter1993,
    DaysBeforeIndependenceDay1pmEarlyCloseAdhoc,
    ChristmasEvesAdhoc,
)
from .nyse import NYSEExchangeCalendar


class IEXExchangeCalendar(NYSEExchangeCalendar):
    """
    Exchange calendar for the Investor's Exchange (IEX).

    IEX Exchange is a U.S. stock exchange focused on driving performance
    for broker-dealers and investors through innovative design and technology.

    Most of this class inherits from NYSEExchangeCalendar since
    the holidays are the same. The only variation is (1) IEX began
    operation in 2013, and (2) IEX has different hours of operation

    References:
    - https://exchange.iex.io/
    - https://iexexchange.io/resources/trading/trading-hours-holidays/index.html
    """

    regular_market_times = {
        "pre": (("2013-03-25", time(8)),),
        "market_open": ((None, time(9, 30)),),
        "market_close": ((None, time(16)),),
        "post": ((None, time(17)),),
    }

    aliases = ["IEX", "Investors_Exchange"]

    @property
    def name(self):
        return "IEX"

    @property
    def full_name(self):
        return "Investor's Exchange"

    @property
    def weekmask(self):
        return "Mon Tue Wed Thu Fri"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USPresidentsDay,
                GoodFriday,
                USMemorialDay,
                USJuneteenthAfter2022,
                USIndependenceDay,
                USThanksgivingDay,
                ChristmasNYSE,
                USMartinLutherKingJrAfter1998,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                ChristmasEvesAdhoc,
            )
        )

    @property
    def special_closes(self):
        return [
            (
                time(hour=13, tzinfo=ZoneInfo("America/New_York")),
                AbstractHolidayCalendar(
                    rules=[
                        DayAfterThanksgiving1pmEarlyCloseInOrAfter1993,
                    ]
                ),
            )
        ]

    """Override NYSE calendar special cases"""

    @property
    def special_closes_adhoc(self):
        return [
            (
                time(13, tzinfo=ZoneInfo("America/New_York")),
                DaysBeforeIndependenceDay1pmEarlyCloseAdhoc,
            )
        ]

    @property
    def special_opens(self):
        return []

    def valid_days(self, start_date, end_date, tz="UTC"):
        start_date = Timestamp(start_date)
        if start_date.tz is not None:
            # Ensure valid Comparison to "2013-08-25" is possible
            start_date.tz_convert(self.tz).tz_localize(None)

        # Limit Start_date to the Exchange's Open
        start_date = max(start_date, Timestamp("2013-08-25"))
        return super().valid_days(start_date, end_date, tz=tz)

    def date_range_htf(
        self,
        frequency: Union[str, Timedelta, int, float],
        start: Union[str, Timestamp, int, float, None] = None,
        end: Union[str, Timestamp, int, float, None] = None,
        periods: Union[int, None] = None,
        closed: Union[Literal["left", "right"], None] = "right",
        *,
        day_anchor: u.Day_Anchor = "SUN",
        month_anchor: u.Month_Anchor = "JAN",
    ) -> DatetimeIndex:

        start, end, periods = u._error_check_htf_range(start, end, periods)

        # Cap Beginning and end dates to the opening date of IEX
        if start is not None:
            start = max(start, Timestamp("2013-08-25"))
        if end is not None:
            end = max(end, Timestamp("2013-08-25"))

        return u.date_range_htf(
            self.holidays(),
            frequency,
            start,
            end,
            periods,
            closed,
            day_anchor=day_anchor,
            month_anchor=month_anchor,
        )
