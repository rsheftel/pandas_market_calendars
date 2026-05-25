"""
KRX Derivatives Futures Calendars
====================================
Korea Exchange (KRX) derivatives market calendars.

All calendars subclass XKRXExchangeCalendar from pandas_market_calendars
(which mirrors exchange_calendars XKRX) to inherit the full Korean
public holiday set, and override regular_market_times for futures hours.

Three products covered, two session structures:

  KRXEquityIndexFuturesCalendar — KOSPI 200 Futures & Options
  KRXGovernmentBondFuturesCalendar — KTB 3/5/10/30 Year Bond Futures
    Both: day session 09:00–15:45 KST + night session 18:00–05:00+1 KST

  KRXFXFuturesCalendar — USD/KRW Futures & Options
    Day session only: 09:00–15:30 KST (no night session)

All times in KST = Asia/Seoul = UTC+9, no DST.

Sources:
  https://global.krx.co.kr/contents/GLB/05/0501/0501010000/GLB0501010000.jsp
  https://global.krx.co.kr/contents/GLB/05/0503/0503010000/GLB0503010000.jsp
"""

from datetime import time
from zoneinfo import ZoneInfo

from pandas_market_calendars.market_calendar import MarketCalendar

from pandas_market_calendars.calendars.mirror import XKRXExchangeCalendar

# Cached XKRX instance — holiday source of truth (sub-ms to instantiate)


class _KRXBase(MarketCalendar):
    """Delegates all holiday logic to the pmc XKRX mirror calendar."""

    _underlying = XKRXExchangeCalendar()

    @property
    def tz(self):
        return ZoneInfo("Asia/Seoul")

    @property
    def regular_holidays(self):
        return self._underlying.regular_holidays

    @property
    def adhoc_holidays(self):
        return self._underlying.adhoc_holidays

    @property
    def special_closes(self):
        return self._underlying.special_closes

    @property
    def special_closes_adhoc(self):
        return self._underlying.special_closes_adhoc


class KRXEquityIndexFuturesCalendar(_KRXBase):
    """
    Korea Exchange — Equity Index Futures & Options
    (KOSPI 200 Futures, KOSPI 200 Options, Mini KOSPI 200 Futures,
     KOSPI 200 Weekly Options, KOSDAQ 150 Futures,
     KRX 300 Futures, Sector Index Futures)

    Day session   (KST = UTC+9): 09:00 – 15:45
    Night session (KST)        : 18:00 – 05:00 next calendar day
    Modelled as: open=09:00, break_start=15:45, break_end=18:00,
                 close=05:00+1.

    Night session is cancelled on the eve of public holidays
    — not modelled (library limitation).

    Holidays: inherited from XKRX (full Korean public holiday set).
    """

    aliases = ["KRX_EQUITY", "KRX_KOSPI200"]

    regular_market_times = {
        "market_open": ((None, time(9, 0)),),
        "market_close": ((None, time(5, 0), 1),),  # 05:00 KST next calendar day
        "break_start": ((None, time(15, 45)),),  # end of day session
        "break_end": ((None, time(18, 0)),),  # start of night session
    }

    @property
    def name(self):
        return "KRX_EQUITY"


class KRXGovernmentBondFuturesCalendar(_KRXBase):
    """
    Korea Exchange — Government Bond (KTB) Futures & Options
    (3 Year KTB Futures & Options,
     5 Year KTB Futures,
     10 Year KTB Futures & Options,
     30 Year KTB Futures,
     Ultra-Long KTB Futures)

    Same session structure as equity index futures.

    Day session   (KST): 09:00 – 15:45
    Night session (KST): 18:00 – 05:00 next calendar day
    Modelled as: open=09:00, break_start=15:45, break_end=18:00,
                 close=05:00+1.

    Holidays: inherited from XKRX.
    """

    aliases = ["KRX_BOND", "KRX_KTB"]

    regular_market_times = {
        "market_open": ((None, time(9, 0)),),
        "market_close": ((None, time(5, 0), 1),),
        "break_start": ((None, time(15, 45)),),
        "break_end": ((None, time(18, 0)),),
    }

    @property
    def name(self):
        return "KRX_BOND"


class KRXFXFuturesCalendar(_KRXBase):
    """
    Korea Exchange — FX Futures & Options
    (USD/KRW Futures & Options,
     EUR/KRW Futures, JPY/KRW Futures, CNH/KRW Futures,
     USD/KRW Weekly Options)

    Day session only — no night session.

    Day session (KST): 09:00 – 15:30
    Modelled as: open=09:00, close=15:30. No break.

    Holidays: inherited from XKRX.
    """

    aliases = ["KRX_FX", "KRX_USDKRW"]

    regular_market_times = {
        "market_open": ((None, time(9, 0)),),
        "market_close": ((None, time(15, 30)),),
    }

    @property
    def name(self):
        return "KRX_FX"
