"""
Taiwan Futures Exchange (TAIFEX, MIC XTAF).

TAIFEX index futures and options trade on the trading days of the Taiwan Stock Exchange (TWSE), in two sessions:

* The regular session, 08:45-13:45 Taipei time (09:00-12:15 before 2001-01-02).
* The after-hours session, 15:00 to 05:00 the next morning, since 2017-05-15. TAIFEX books its trades to the NEXT
  trading day, so a trading day starts at 15:00 on the previous trading day. Unlike the China futures night
  sessions, it also runs on the evening before a closure: Monday's trading day starts on Friday afternoon, and the
  session that opens on the last trading day before Lunar New Year belongs to the first trading day after it.

``TAIFEX`` (aliases ``XTAF``, ``TAIFEX_TX``) is the TAIEX futures and options group, which shares these sessions:
TAIEX futures (TX), mini and micro TAIEX futures (MTX, TMF), TAIEX options (TXO) and the other domestic index
futures with the same hours, such as the electronics and finance sector futures (TE, TF). Its after-hours history
is that of TX; products that joined the after-hours session later (TE in 2018, TF in 2025) are covered from then.
``TAIFEX_Day`` is the regular session alone.

Not covered: products with other hours (FX and gold futures 08:45-16:15, stock futures and options, TOPIX futures
08:00-16:15, all with after-hours from 17:25), the 13:30 close of an expiring contract on its last trading day, and
Saturday sessions. TAIFEX traded on Saturdays until 2000 and on Saturday make-up workdays until 2018-12-22; a
Monday-Friday weekmask cannot express those days (issue #480), so they are missing from the calendar.

Closures are TWSE's: the XTAI rules from exchange_calendars plus ``TAIFEX_ADHOC_CLOSURES``. Trading days and
after-hours sessions match TAIFEX's daily TX data from 2002-01-01 to 2026-11-26, apart from the Saturday sessions.
Before 2002 the XTAI closures differ from TAIFEX's on a few days.

Sources: TAIFEX contract specifications (https://www.taifex.com.tw/enl/eng2/tX), after-hours trading
(https://www.taifex.com.tw/enl/eng4/aHIntroduction), trading-hour history
(https://www.taifex.com.tw/cht/4/historyOfTrading), trading calendars, closure notices and daily market data;
see ``pandas_market_calendars.sources`` and ``holidays/taifex.py``.
"""

from datetime import time
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
from pandas.tseries.holiday import AbstractHolidayCalendar

from pandas_market_calendars.holidays.taifex import AFTER_HOURS_FROM, NO_AFTER_HOURS, TAIFEX_ADHOC_CLOSURES
from pandas_market_calendars.market_calendar import MarketCalendar


# The regular session moved from 09:00-12:15 to 08:45-13:45 on this date.
REGULAR_HOURS_FROM = "2001-01-02"
REGULAR_OPEN = time(8, 45)
REGULAR_CLOSE = time(13, 45)
DAY_OPEN = ((None, time(9)), (REGULAR_HOURS_FROM, REGULAR_OPEN))
DAY_CLOSE = ((None, time(12, 15)), (REGULAR_HOURS_FROM, REGULAR_CLOSE))
AFTER_HOURS_OPEN = time(15)
AFTER_HOURS_CLOSE = time(5)


class TAIFEXDayCalendar(MarketCalendar):
    """
    Taiwan Futures Exchange, regular session only: 08:45-13:45 Taipei time (09:00-12:15 before 2001-01-02).
    https://www.taifex.com.tw/enl/eng2/tX
    """

    aliases = ["TAIFEX_Day"]
    regular_market_times = {"market_open": DAY_OPEN, "market_close": DAY_CLOSE}

    @property
    def name(self) -> str:
        return "TAIFEX_Day"

    @property
    def full_name(self) -> str:
        return "Taiwan Futures Exchange"

    @property
    def tz(self) -> ZoneInfo:
        return ZoneInfo("Asia/Taipei")

    @staticmethod
    def _xtai() -> Any:
        """
        The Taiwan Stock Exchange calendar mirrored from exchange_calendars. TAIFEX index products trade on TWSE
        trading days, so its holiday rules are reused rather than copied (the lunar holidays are listed there).

        :return: the XTAI calendar
        """
        return MarketCalendar.factory("XTAI")

    @property
    def regular_holidays(self) -> AbstractHolidayCalendar | None:
        return self._xtai().regular_holidays

    @property
    def adhoc_holidays(self) -> list[Any]:
        return [*self._xtai().adhoc_holidays, *TAIFEX_ADHOC_CLOSURES]


class TAIFEXExchangeCalendar(TAIFEXDayCalendar):
    """
    Taiwan Futures Exchange, TAIEX futures and options group, with the after-hours session.

    A trading day opens with the after-hours session at 15:00 on the previous trading day (``market_open``), pauses
    at 05:00 (``night_close``) and continues with the regular session from 08:45 (``day_open``) to 13:45
    (``market_close``), Taipei time. Before 2017-05-16, and on the days in ``NO_AFTER_HOURS``, there is no
    after-hours session: ``market_open``, ``night_close`` and ``day_open`` are all the regular open.
    https://www.taifex.com.tw/enl/eng4/aHIntroduction
    """

    aliases = ["TAIFEX", "XTAF", "TAIFEX_TX"]
    regular_market_times = {
        "market_open": (*DAY_OPEN, (AFTER_HOURS_FROM, AFTER_HOURS_OPEN, -1)),
        "night_close": (*DAY_OPEN, (AFTER_HOURS_FROM, AFTER_HOURS_CLOSE)),
        "day_open": DAY_OPEN,
        "market_close": DAY_CLOSE,
    }
    open_close_map = {**MarketCalendar.open_close_map, "night_close": False, "day_open": True}

    @property
    def name(self) -> str:
        return "TAIFEX"

    def _after_hours_gaps(self) -> pd.Series:
        """
        Trading days whose after-hours session opened more than one calendar day earlier: Mondays and the first
        trading days after closures. The session always opens on the previous trading day, so the gap is computed
        from the trading days themselves, and future holidays need no extra code.

        :return: number of calendar days since the previous trading day (2 or more), indexed by trading day
        """
        # start two weeks early so that the first after-hours day also has a previous trading day
        start = pd.Timestamp(AFTER_HOURS_FROM) - pd.Timedelta(days=14)
        days = self.valid_days(start, "2100-12-31", tz=None)
        gaps = pd.Series((days[1:] - days[:-1]).days, index=days[1:])
        keep = (gaps.index >= pd.Timestamp(AFTER_HOURS_FROM)) & (gaps > 1) & ~gaps.index.isin(NO_AFTER_HOURS)
        return gaps[keep]

    def _after_hours_specials(self, market_time: time, offset: int) -> list[Any]:
        """
        Special times of one after-hours market time: shifted back by the gap on Mondays and after closures, and
        conformed to the regular open on the trading days without an after-hours session.

        :param market_time: the regular local time of the market time
        :param offset: its regular day offset relative to the trading day
        :return: list of ((time, day offset), dates) and (time, dates) tuples
        """
        gaps = self._after_hours_gaps()
        shifted = [((market_time, offset + 1 - int(gap)), gaps.index[gaps == gap]) for gap in sorted(gaps.unique())]
        return [*shifted, (REGULAR_OPEN, pd.DatetimeIndex(NO_AFTER_HOURS))]

    @property
    def special_opens_adhoc(self) -> list[Any]:
        return self._after_hours_specials(AFTER_HOURS_OPEN, -1)

    @property
    def special_night_close_adhoc(self) -> list[Any]:
        return self._after_hours_specials(AFTER_HOURS_CLOSE, 0)
