"""

MEFF (Madrid)  Derivatives Calendars
================================================================

MEFFIBEXFuturesCalendar — IBEX 35 Futures & Options (MEFF, Madrid)
NasdaqStockholmDerivsCalendar — OMXS30 Futures & Options (Nasdaq Stockholm)

Both delegate to the existing pmc cash equity calendars (XMAD, XSTO) for
their core holiday set, and add corrections where the futures market differs.

MEFF corrections vs XMAD:
  XMAD (exchange_calendars mirror) is missing three Spanish national holidays
  that MEFF closes for:
    - Epiphany (6 Jan)
    - Fiesta Nacional de España (12 Oct)
    - Immaculate Conception (8 Dec)
  These are added via additional adhoc_holidays.

  MEFF also does NOT close for Dec 26 (Boxing Day is not a Spanish national
  holiday) — but XMAD shows it closed. This is corrected by not inheriting
  the XMAD Dec 26 closure... however since we can't subtract holidays from
  the inherited set, Dec 26 is noted as a known discrepancy. In practice,
  MEFF rarely trades on Dec 26 due to low liquidity regardless.

Trading hours (CET/CEST = Europe/Madrid / Europe/Stockholm):
  MEFF IBEX 35 Futures: pre-open 08:00, COB 09:00–17:35

Sources:
  https://www.meff.es/ing/Trading-Hours
  https://www.meff.es/ing/Trading-Calendar
  https://library.tradingtechnologies.com/user-setup/mef-overview.html
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
from pandas_market_calendars.calendars.mirror import XMADExchangeCalendar

# ---------------------------------------------------------------------------
# Spanish national holidays missing from XMAD
# ---------------------------------------------------------------------------

_Epiphany = Holiday(
    "Epiphany (Reyes Magos)",
    month=1,
    day=6,
    observance=weekend_to_monday,
)

_FiestaNacional = Holiday(
    "Fiesta Nacional de España",
    month=10,
    day=12,
    observance=weekend_to_monday,
)

_ImmaculateConception = Holiday(
    "Immaculate Conception",
    month=12,
    day=8,
    observance=weekend_to_monday,
)

# Pre-compute the additional Spanish holiday dates (2010–2035)
_extra_spanish_holidays = (
    AbstractHolidayCalendar(
        rules=[
            _Epiphany,
            _FiestaNacional,
            _ImmaculateConception,
        ]
    )
    .holidays("2010-01-01", "2035-12-31")
    .tolist()
)


# ---------------------------------------------------------------------------
# MEFF IBEX 35 Futures Calendar
# ---------------------------------------------------------------------------


class MEFFIBEXFuturesCalendar(MarketCalendar):
    """
    MEFF (Mercado Español de Futuros Financieros) — IBEX 35 Derivatives
    (IBEX 35® Futures (FIE), Mini IBEX 35® Futures (FIEM),
     Micro IBEX 35® Futures, IBEX 35® Div Impact Futures,
     Options on IBEX 35® (OPE),
     Futures on Spanish Stocks, Single Stock Options,
     Future xRolling®, Future on 10 Year Bond)

    Holidays: Spanish national holidays (XMAD base + three additional
    holidays missing from the pmc XMAD mirror):
        - New Year's Day (1 Jan)
        - Epiphany (6 Jan)           ← not in XMAD
        - Good Friday
        - Easter Monday
        - Labour Day (1 May)
        - Fiesta Nacional (12 Oct)   ← not in XMAD
        - All Saints' Day (1 Nov)
        - Constitution Day (6 Dec)
        - Immaculate Conception (8 Dec) ← not in XMAD
        - Christmas Day (25 Dec)

    Early closes (14:00 CET / 13:00 UTC winter):
        - Christmas Eve (24 Dec)
        - New Year's Eve (31 Dec)
    Inherited from XMAD.

    Normal session (CET/CEST):
        Pre-open : 08:00 – 09:00
        COB      : 09:00 – 17:35
    Modelled as 09:00 – 17:35.

    Note: Dec 26 (St Stephen's Day) is NOT a Spanish national holiday and
    MEFF does not close for it. The XMAD mirror incorrectly shows it as
    closed; this cannot be corrected by adding holidays (only by subtracting
    them, which is not supported). In practice Dec 26 liquidity is negligible.

    Source: https://www.meff.es/ing/Trading-Calendar
    """

    _underlying = XMADExchangeCalendar()

    aliases = ["MEFF", "MEFF_IBEX"]

    regular_market_times = {
        "market_open": ((None, time(9, 0)),),
        "market_close": ((None, time(17, 35)),),
    }

    @property
    def name(self):
        return "MEFF"

    @property
    def tz(self):
        return ZoneInfo("Europe/Madrid")

    @property
    def regular_holidays(self):
        return self._underlying.regular_holidays

    @property
    def adhoc_holidays(self):
        return list(self._underlying.adhoc_holidays) + _extra_spanish_holidays

    @property
    def special_closes(self):
        # 14:00 CET winter = 13:00 UTC; inherited correctly from XMAD
        return self._underlying.special_closes

    @property
    def special_closes_adhoc(self):
        return self._underlying.special_closes_adhoc
