from datetime import time
from typing import Any, Literal

from pandas import DatetimeIndex, Timedelta, Timestamp

from pandas_market_calendars import calendar_utils as u

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
    def name(self) -> str:
        return "IEX"

    @property
    def full_name(self) -> str:
        return "Investor's Exchange"

    @property
    def weekmask(self) -> str:
        return "Mon Tue Wed Thu Fri"

    @property
    def special_opens(self) -> list[Any]:
        return []

    def valid_days(self, start_date: Any, end_date: Any, tz: Any = "UTC") -> DatetimeIndex:
        start_date = Timestamp(start_date)
        if start_date.tz is not None:
            # Ensure valid Comparison to "2013-08-25" is possible
            start_date.tz_convert(self.tz).tz_localize(None)

        # Limit Start_date to the Exchange's Open
        start_date = max(start_date, Timestamp("2013-08-25"))
        return super().valid_days(start_date, end_date, tz=tz)

    def date_range_htf(
        self,
        frequency: str | Timedelta | int | float,
        start: str | Timestamp | int | float | None = None,
        end: str | Timestamp | int | float | None = None,
        periods: int | None = None,
        closed: Literal["left", "right"] | None = "right",
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
