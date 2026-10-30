"""
Nasdaq Stockholm (OMX) Derivatives Calendars
================================================================

NasdaqStockholmDerivsCalendar — OMXS30 Futures & Options (Nasdaq Stockholm)

Delegates to the existing pmc cash equity calendar XSTO for
their core holiday set, and add corrections where the futures market differs.


Nasdaq Stockholm corrections vs XSTO:
  XSTO appears correct for all Swedish holidays. No corrections needed.
  Whit Monday (Pingstdagen) shows OPEN in pmc but the Stockholm exchange
  does close — however this appears to be a pmc data issue in the mirror;
  it IS closed per exchange_calendars.

Trading hours (CET/CEST = Europe/Madrid / Europe/Stockholm):
  Nasdaq Stockholm OMXS30 Futures: 09:00–17:30

Sources:
  https://www.nasdaq.com/solutions/nasdaq-nordic-markets
"""

from datetime import time
from zoneinfo import ZoneInfo

import pandas as pd
import pandas_market_calendars as mcal
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    Holiday,
    weekend_to_monday,
)
from pandas_market_calendars.market_calendar import MarketCalendar

from pandas_market_calendars.calendars.mirror import XSTOExchangeCalendar

# ---------------------------------------------------------------------------
# Nasdaq Stockholm OMXS30 Futures Calendar
# ---------------------------------------------------------------------------


class NasdaqStockholmDerivsCalendar(MarketCalendar):
    """
    Nasdaq Stockholm — Equity Index Derivatives
    (OMXS30 Index Futures, OMXS30 Index Options,
     Swedish Single Stock Futures & Options)

    Holidays: Swedish public holidays, fully inherited from XSTO:
        - New Year's Day (1 Jan)
        - Epiphany / Trettondag (6 Jan)
        - Good Friday
        - Easter Monday
        - Labour Day (1 May)
        - Ascension Day (Kristi Himmelsfärdsdag)
        - Midsummer Eve (Midsommarafton — Friday before Midsummer Day)
        - All Saints' Day (Alla Helgons dag — Saturday closest to Nov 1)
        - Christmas Eve (24 Dec) — fully closed
        - Christmas Day (25 Dec) — fully closed
        - Boxing Day (26 Dec) — fully closed
        - New Year's Eve (31 Dec) — fully closed

    Early closes (inherited from XSTO):
        - Maundy Thursday (Skärtorsdagen): 13:00 CET
        - Midsummer Eve: 13:00 CET (where it falls on a Friday)

    Normal session (CET/CEST = Europe/Stockholm):
        09:00 – 17:30

    Source: https://www.nasdaq.com/solutions/nasdaq-nordic-markets
    """

    _underlying = XSTOExchangeCalendar()

    aliases = ["OMXS", "OMXS30"]

    regular_market_times = {
        "market_open": ((None, time(9, 0)),),
        "market_close": ((None, time(17, 30)),),
    }

    @property
    def name(self):
        return "OMXS"

    @property
    def tz(self):
        return ZoneInfo("Europe/Stockholm")

    @property
    def regular_holidays(self):
        return self._underlying.regular_holidays

    @property
    def adhoc_holidays(self):
        return list(self._underlying.adhoc_holidays)

    @property
    def special_closes(self):
        # 13:00 local CET on Maundy Thursday and Midsummer Eve
        return self._underlying.special_closes

    @property
    def special_closes_adhoc(self):
        return self._underlying.special_closes_adhoc
