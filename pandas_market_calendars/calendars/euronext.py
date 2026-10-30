"""
Euronext Derivatives Exchange Calendars
========================================
Thin wrappers over the existing pandas_market_calendars cash equity calendars
(XPAR, XAMS, XBRU, XLIS, XMIL, XOSL) that inherit all holiday, early-close,
and special-close logic but replace trading hours with derivatives session times.

Holiday correctness is fully delegated to the underlying cash calendars —
no holiday logic is duplicated here. If the upstream calendar is updated,
these automatically benefit.

Trading hours sourced from:
    Euronext Derivatives Trading Hours schedule (effective 2 February 2026)
    https://live.euronext.com/en/media/295/download

All times are local CET/CEST (Europe/Paris) unless noted.
Oslo uses CET/CEST (Europe/Oslo, same offset).

Key hours by market (normal trading day, Central Order Book):
    AEX / CAC 40 / FTSE MIB index futures : 07:30 – 22:00
    BEL 20 / PSI / Single Stock Futures    : 07:30 – 17:40  (07:30–18:30 LiS)
    OBX (Oslo) index futures               : 07:30 – 16:20
    Paris commodities (wheat, rapeseed…)   : 07:30 – 18:30

Half-trading-day closes (inherited from cash calendars via special_closes):
    Amsterdam/Brussels/Lisbon/Paris : 13:55 CET
    Oslo                            : 13:00 CET
    Milan                           : No scheduled half days
"""

from datetime import time
from zoneinfo import ZoneInfo
from functools import cached_property

from pandas_market_calendars.market_calendar import MarketCalendar
from pandas_market_calendars.calendars.mirror import (
    XPARExchangeCalendar,
    XAMSExchangeCalendar,
    XBRUExchangeCalendar,
    XLISExchangeCalendar,
    XMILExchangeCalendar,
    XOSLExchangeCalendar,
)


class _EuronextDerivsMixin:
    """
    Mixin that delegates regular_holidays, adhoc_holidays, special_closes,
    and special_closes_adhoc to a cash calendar instance (_cash_cal).
    Subclasses must set _cash_cal at class level and define
    regular_market_times, name, and tz.
    """

    _cash_cal = None  # set in each subclass
    _half_day_close_time = None  # Ditto

    @property
    def regular_holidays(self):
        return self._cash_cal.regular_holidays

    @property
    def adhoc_holidays(self):
        return self._cash_cal.adhoc_holidays

    @property
    def special_closes(self):
        return [(self._half_day_close_time, hol_cal) for _, hol_cal in self._cash_cal.special_closes]

    @property
    def special_closes_adhoc(self):
        return [(self._half_day_close_time, hol_cal) for _, hol_cal in self._cash_cal.special_closes_adhoc]



class EuronextParisIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Paris — Index & Equity Derivatives
    (CAC 40 Futures/Mini/Weekly)

    Other futures have reduced hours vs this.

    Normal session (CET/CEST):
        Call phase : 07:30 – 08:00
        COB        : 08:00 – 22:00
    Modelled as 08:30 – 22:00.

    Half-trading-day close: 14:00 CET (dates inherited from XPAR).
    Holidays: inherited from XPAR.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_PAR_INDEX", "ENX_FCE"]

    @cached_property
    def _cash_cal(self):
        return XPARExchangeCalendar()

    _half_day_close_time = time(14, 0)

    regular_market_times = {
        "market_open": ((None, time(8, 0)),),
        "market_close": ((None, time(22, 0)),),
    }

    @property
    def name(self):
        return "ENX_PAR_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Paris")



class EuronextAmsterdamIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Amsterdam — Index & Equity Derivatives
    (AEX Futures FTI, AEX Mini MFA, AEX Weeklies _FT,
     AEX Dividend AXF)

    Note this does not cover AMX index, single stock & power futures, 
    or any options, which are all open less.

    Normal session (CET/CEST):
        AEX index futures COB: 08:00 – 22:00  (call 07:30–08:00)
    Modelled as 07:30 – 22:00 (widest window — AEX futures).

    Half-trading-day close: 14:00 CET.
    Holidays: inherited from XAMS (identical to XPAR).

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_AMS_INDEX", "ENX_FTI", "ENX_AEX"]
    
    @cached_property
    def _cash_cal(self):
        return XAMSExchangeCalendar()

    _half_day_close_time = time(14, 0)

    regular_market_times = {
        "market_open": ((None, time(8, 0)),),
        "market_close": ((None, time(22, 0)),),
    }

    @property
    def name(self):
        return "ENX_AMS_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Amsterdam")



class EuronextBrusselsIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Brussels — Index & Equity Derivatives
    (BEL 20 Futures BXF)

    Single stock futures are mostly the same except for slightly different closing times
    on half days.

    Normal session (CET/CEST):
        Call phase : 07:30 – 09:01
        COB        : 09:01 – 17:40
    Modelled as 09:01 – 17:40.

    Half-trading-day close: 14:00 CET.
    Holidays: inherited from XBRU (identical to XPAR).

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_BRU_INDEX", "ENX_BXF", "ENX_BEL20"]
    
    @cached_property
    def _cash_cal(self):
        return XBRUExchangeCalendar()

    _half_day_close_time = time(14, 0)

    regular_market_times = {
        "market_open": ((None, time(9, 1)),),
        "market_close": ((None, time(17, 40)),),
    }

    @property
    def name(self):
        return "ENX_BRU_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Brussels")



class EuronextLisbonIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Lisbon — Index & Equity Derivatives
    (PSI Futures PSI)

    Single stocks futures are mostly the same hours and holidays, just slightly
    different half day closing times.

    Normal session (WET/WEST = UTC+0/+1):
        Call phase : 07:30 – 09:01 CET  (06:30–08:01 local)
        COB        : 09:01 – 17:40 CET  (08:01–16:40 local)
    Modelled in CET as 09:01 – 17:40 (times published in CET).
    Timezone set to Europe/Lisbon (UTC+0 winter, UTC+1 summer).

    Half-trading-day close: 13:55 CET local (on dates inherited from XLIS).
    Holidays: inherited from XLIS (identical to XPAR).

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_LIS_INDEX", "ENX_PSI"]
    
    @cached_property
    def _cash_cal(self):
        return XLISExchangeCalendar()

    _half_day_close_time = time(13, 55)

    regular_market_times = {
        # Times published as CET; Lisbon is UTC+0/+1, so 1h behind CET 
        # Storing as local Lisbon time: 08:01 – 16:40
        "market_open": ((None, time(8, 1)),),
        "market_close": ((None, time(16, 40)),),
    }

    @property
    def name(self):
        return "ENX_LIS_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Lisbon")

class EuronextMilanIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Milan — Index & Equity Derivatives
    (FTSE MIB Futures FIB, Mini MIN, Micro MICR)

    Hours for other futures are less than here.

    Normal session (CET/CEST):
        FTSE MIB index futures COB: 08:00 – 22:00  (call 07:30–08:00)
    Modelled as 08:00 – 22:00.

    Milan is FULLY CLOSED on Christmas Eve (24 Dec) and New Year's Eve
    (31 Dec) — not a half day, unlike other Euronext markets.
    This is already correctly modelled in XMIL which this calendar inherits.

    Holidays: inherited from XMIL.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_MIL_INDEX", "ENX_FIB", "ENX_FTSEMIB"]

    @cached_property
    def _cash_cal(self):
        return XMILExchangeCalendar()

    # No half days, so no half day close time set.

    regular_market_times = {
        "market_open": ((None, time(8, 0)),),
        "market_close": ((None, time(22, 0)),),
    }

    @property
    def name(self):
        return "ENX_MIL_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Rome")



class EuronextOsloIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Oslo Børs — Index & Equity Derivatives
    (OBX Total Return Futures OBF, Single Stock Futures OF.,
     OBX Index Options OBX, Individual Equity Options OO.)

    Normal session (CET/CEST):
        Call phase : 07:30 – 09:01
        COB        : 09:01 – 16:20
    Modelled as 09:01 – 16:20.

    Oslo-specific closures (additional vs core Euronext):
        - Maundy Thursday (Thu before Easter)
        - Ascension Day (39 days after Easter, always Thursday)
        - Whit Monday (49 days after Easter + 1)
        - Constitution Day (17 May) (Ascencion day?)
        - Christmas Eve (24 Dec) — fully closed, not half day
        - New Year's Eve (31 Dec) — fully closed, not half day
    Half-trading-day:
        - Wednesday before Easter - close at 1pm.
    All inherited from XOSL.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_OSL_INDEX", "ENX_OBF", "ENX_OBX"]
    
    @cached_property
    def _cash_cal(self):
        return XOSLExchangeCalendar()

    _half_day_close_time = time(13, 0)

    regular_market_times = {
        "market_open": ((None, time(9, 1)),),
        "market_close": ((None, time(16, 20)),),
    }

    @property
    def name(self):
        return "ENX_OSL_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Oslo")




class EuronextParisCommodityDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Paris — Commodity Derivatives
    (Milling Wheat YF.EBM/YO.OBM, Rapeseed YF.ECO/YO.OCO,
     Corn YF.EMA/YO.OMA)

    Durum, Salmon, Spreads, TAS & Freight all have different hours.

    Normal session (CET/CEST):
        Wheat/Rape/Corn call phase : 07:30 – 10:45
        Wheat/Rape/Corn COB        : 10:45 – 20:15
    
    Hours on 3 days leading into expiry are reduced, but this library
    doesn't have a language to support that.

    Modelled as 10:45 – 20:15 

    Half-trading-day close: 14:00 CET (inherited from XPAR).
    Note: no expiries on half-trading days per Euronext rules.
    Holidays: inherited from XPAR.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_PAR_COMM", "ENX_WHEAT", "ENX_AGRI"]
    
    @cached_property
    def _cash_cal(self):
        return XPARExchangeCalendar()

    _half_day_close_time = time(14, 0)

    regular_market_times = {
        "market_open": ((None, time(10, 45)),),
        "market_close": ((None, time(20, 15)),),
    }

    @property
    def name(self):
        return "ENX_PAR_COMM"

    @property
    def tz(self):
        return ZoneInfo("Europe/Paris")
