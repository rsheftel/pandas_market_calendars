"""
US equity exchanges with a 23/5 overnight session: Nasdaq and NYSE Arca.

From Sunday 2026-12-06 both exchanges add an overnight session from 21:00 to 04:00 ET, Sunday to Thursday
nights, followed by the existing 04:00-20:00 day session. Trades in the overnight session count toward the
next trading date, so trading date D starts at 21:00 on the previous calendar day (D-1). The overnight
session is therefore a market time with a -1 day offset, the same approach the China futures night sessions use.

Holidays and early closes follow NYSE, so both calendars subclass NYSEExchangeCalendar. Because the overnight
session always opens on the evening before a valid trading day, holidays need no special handling: Monday opens
on Sunday evening, the day after a holiday opens on the holiday's evening, and a holiday has no session at all.

The "NASDAQ" alias still points at NYSEExchangeCalendar, so existing schedules are unchanged. The calendars here
are registered under new names only.
"""

from datetime import time
from typing import Any

from .nyse import NYSEExchangeCalendar


#: First trading date with an overnight session. Its session opens at 21:00 ET on the previous calendar day
#: (Sunday 2026-12-06). Change this one value if the industry launch date moves.
OVERNIGHT_FROM = "2026-12-07"


def overnight_market_times(base: Any) -> dict:
    """
    Add the 23/5 overnight session to a set of US equity market times.

    Before OVERNIGHT_FROM the overnight time equals pre (04:00), so the session has zero length and historical
    schedules are unchanged. From OVERNIGHT_FROM it opens at 21:00 on the previous calendar day and runs into
    pre at 04:00.

    :param base: regular_market_times of the calendar being extended.
    :return: regular_market_times with an "overnight" entry added.
    """
    return {"overnight": ((None, time(4)), (OVERNIGHT_FROM, time(21), -1)), **base}


class NASDAQExchangeCalendar(NYSEExchangeCalendar):
    """
    Exchange calendar for the Nasdaq Stock Market with the 23/5 overnight session.

    Holidays and early closes follow NYSE. From 2026-12-07 the trading day starts with an overnight session at
    21:00 ET on the previous evening (Sunday to Thursday nights), followed by the 04:00-20:00 day session. The
    default schedule() columns (market_open, market_close) are the same as NYSE; use start="overnight" to
    include the overnight session.

    To move the start date, for example if the launch is delayed:
    cal.change_time("overnight", ((None, time(4)), ("2027-01-25", time(21), -1)))

    The "NASDAQ" alias still returns NYSEExchangeCalendar; this calendar is registered as "NASDAQ_23_5".

    References:
    - SR-NASDAQ-2025-109 (23/5 rule filing)
    """

    aliases = ["NASDAQ_23_5"]
    regular_market_times = overnight_market_times(NYSEExchangeCalendar.regular_market_times)
    # The overnight session is an opening time; it runs straight into pre at 04:00, so it needs no closing time.
    open_close_map = {**NYSEExchangeCalendar.open_close_map, "overnight": True}

    @property
    def name(self) -> str:
        return "NASDAQ_23_5"

    @property
    def full_name(self) -> str:
        return "Nasdaq Stock Market (23/5)"


class NYSEArcaExchangeCalendar(NYSEExchangeCalendar):
    """
    Exchange calendar for NYSE Arca with the overnight session.

    Holidays and early closes follow NYSE. From 2026-12-07 the trading day starts with an overnight session at
    21:00 ET on the previous evening (Sunday to Thursday nights). Arca calls its sessions Overnight, Early, Core
    and Late; they map onto overnight, pre, market_open..market_close and post. Use start="overnight" in
    schedule() to include the overnight session.

    To move the start date, for example if the launch is delayed:
    cal.change_time("overnight", ((None, time(4)), ("2027-01-25", time(21), -1)))

    References:
    - SR-NYSEArca-2026-53 (overnight session rule filing)
    """

    aliases = ["NYSE_Arca", "ARCA", "ARCX"]
    regular_market_times = overnight_market_times(NYSEExchangeCalendar.regular_market_times)
    open_close_map = {**NYSEExchangeCalendar.open_close_map, "overnight": True}

    @property
    def name(self) -> str:
        return "NYSE_Arca"

    @property
    def full_name(self) -> str:
        return "NYSE Arca"
