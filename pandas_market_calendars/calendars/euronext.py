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
    Amsterdam/Brussels/Lisbon/Paris : 14:05 CET
    Dublin                          : 13:28–13:30 local
    Milan / Oslo                    : fully closed (not half-day)
"""

from datetime import time
from zoneinfo import ZoneInfo

import pandas_market_calendars as mcal
from pandas_market_calendars.market_calendar import MarketCalendar

# ---------------------------------------------------------------------------
# Cached cash calendar instances — holiday source of truth
# ---------------------------------------------------------------------------
_xpar = mcal.get_calendar("XPAR")   # Paris  — same holidays as AMS/BRU/LIS
_xams = mcal.get_calendar("XAMS")   # Amsterdam
_xbru = mcal.get_calendar("XBRU")   # Brussels
_xlis = mcal.get_calendar("XLIS")   # Lisbon
_xmil = mcal.get_calendar("XMIL")   # Milan
_xosl = mcal.get_calendar("XOSL")   # Oslo


# ---------------------------------------------------------------------------
# Helper mixin — delegates all holiday properties to a cash calendar instance
# ---------------------------------------------------------------------------

class _EuronextDerivsMixin:
    """
    Mixin that delegates regular_holidays, adhoc_holidays, special_closes,
    and special_closes_adhoc to a cash calendar instance (_cash_cal).
    Subclasses must set _cash_cal at class level and define
    regular_market_times, name, and tz.
    """
    _cash_cal = None  # set in each subclass

    @property
    def regular_holidays(self):
        return self._cash_cal.regular_holidays

    @property
    def adhoc_holidays(self):
        return self._cash_cal.adhoc_holidays

    @property
    def special_closes(self):
        return self._cash_cal.special_closes

    @property
    def special_closes_adhoc(self):
        return self._cash_cal.special_closes_adhoc


# ---------------------------------------------------------------------------
# 1. Euronext Paris Derivatives
#    CAC 40® Index Futures (FCE), CAC 40® Mini (MFC), CAC 40® Weeklies (_FC)
#    FTSE MIB Total Return (FIT), CAC 40 Total Return (FCT)
#    FTSEurofirst 80/100 (FEF/FEO), EPRA/NAREIT (EPR/EPE)
#    Euronext Eurozone Banks Index (EBF), ESG Large 80 (ESG)
#    ISEQ 20® (ISE), Paris Single Stock Futures (PF.)
#
#    COB: 08:00–22:00  (call phase 07:30–08:00)
#    Modelled open: 07:30 (call phase start)
# ---------------------------------------------------------------------------

class EuronextParisIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Paris — Index & Equity Derivatives
    (CAC 40 Futures/Mini/Weekly FCE/MFC/_FC, Total Return FCT/FIT,
     FTSEurofirst FEF/FEO, EPRA EPR/EPE, Banks EBF/EBD, ESG, ISEQ ISE,
     Paris Single Stock Futures PF.)

    Normal session (CET/CEST):
        Call phase : 07:30 – 08:00
        COB        : 08:00 – 22:00
    Modelled as 07:30 – 22:00.

    Half-trading-day close: 14:05 CET (inherited from XPAR).
    Holidays: inherited from XPAR.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_PAR_INDEX", "ENX_FCE"]
    _cash_cal = _xpar

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(22, 0)),),
    }

    @property
    def name(self):
        return "ENX_PAR_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Paris")


# ---------------------------------------------------------------------------
# 2. Euronext Amsterdam Derivatives
#    AEX-Index® Futures (FTI), AEX Mini (MFA), AEX Weeklies (_FT)
#    AEX Dividend Index (AXF), AMX-Index® (FMX)
#    Amsterdam Single Stock Futures (AF.), Amsterdam Power Futures (RF.)
# ---------------------------------------------------------------------------

class EuronextAmsterdamIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Amsterdam — Index & Equity Derivatives
    (AEX Futures FTI, AEX Mini MFA, AEX Weeklies _FT,
     AEX Dividend AXF, AMX FMX, Single Stock Futures AF.,
     Power Futures RF.)

    Normal session (CET/CEST):
        AEX index futures COB: 08:00 – 22:00  (call 07:30–08:00)
        AEX options / SSF    : 09:01 – 17:30/17:40
    Modelled as 07:30 – 22:00 (widest window — AEX futures).

    Half-trading-day close: 14:05 CET (inherited from XAMS).
    Holidays: inherited from XAMS (identical to XPAR).

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_AMS_INDEX", "ENX_FTI", "ENX_AEX"]
    _cash_cal = _xams

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(22, 0)),),
    }

    @property
    def name(self):
        return "ENX_AMS_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Amsterdam")


# ---------------------------------------------------------------------------
# 3. Euronext Brussels Derivatives
#    BEL 20® Futures (BXF), Brussels Single Stock Futures (BF.)
#
#    COB: 09:01–17:40  (call phase 07:30–09:01)
#    Modelled as 07:30 – 17:40
# ---------------------------------------------------------------------------

class EuronextBrusselsIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Brussels — Index & Equity Derivatives
    (BEL 20 Futures BXF, Single Stock Futures BF.)

    Normal session (CET/CEST):
        Call phase : 07:30 – 09:01
        COB        : 09:01 – 17:40
    Modelled as 07:30 – 17:40.

    Half-trading-day close: 14:05 CET (inherited from XBRU).
    Holidays: inherited from XBRU (identical to XPAR).

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_BRU_INDEX", "ENX_BXF", "ENX_BEL20"]
    _cash_cal = _xbru

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(17, 40)),),
    }

    @property
    def name(self):
        return "ENX_BRU_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Brussels")


# ---------------------------------------------------------------------------
# 4. Euronext Lisbon Derivatives
#    PSI Futures (PSI), Lisbon Single Stock Futures (SF.)
#
#    COB: 09:01–17:40  (call phase 07:30–09:01)
# ---------------------------------------------------------------------------

class EuronextLisbonIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Lisbon — Index & Equity Derivatives
    (PSI Futures PSI, Single Stock Futures SF.)

    Normal session (WET/WEST = UTC+0/+1):
        Call phase : 07:30 – 09:01 CET  (06:30–08:01 local)
        COB        : 09:01 – 17:40 CET  (08:01–16:40 local)
    Modelled in CET as 07:30 – 17:40 (times published in CET).
    Timezone set to Europe/Lisbon (UTC+0 winter, UTC+1 summer).

    Half-trading-day close: 14:05 CET / 13:05 local (inherited from XLIS).
    Holidays: inherited from XLIS (identical to XPAR).

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_LIS_INDEX", "ENX_PSI"]
    _cash_cal = _xlis

    regular_market_times = {
        # Times published as CET; Lisbon is UTC+0/+1, so 1h behind CET in winter.
        # Storing as local Lisbon time: 06:30 – 16:40
        "market_open":  ((None, time(6, 30)),),
        "market_close": ((None, time(16, 40)),),
    }

    @property
    def name(self):
        return "ENX_LIS_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Lisbon")


# ---------------------------------------------------------------------------
# 5. Euronext Milan Derivatives
#    FTSE MIB Index Futures (FIB), Mini (MIN), Micro (MICR)
#    FTSE MIB Dividend (FDIV), PIR PMI TR (MCAP)
#    Bond Mini-futures (TF.M), Milan Single Stock Futures (EF.)
#
#    COB: 08:00–22:00  (call phase 07:30–08:00)
#    Milan is fully closed on Xmas Eve and NYE (not a half day).
# ---------------------------------------------------------------------------

class EuronextMilanIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Milan — Index & Equity Derivatives
    (FTSE MIB Futures FIB, Mini MIN, Micro MICR,
     Dividend FDIV, PIR MCAP, Bond Mini-futures TF.M,
     Single Stock Futures EF.)

    Normal session (CET/CEST):
        FTSE MIB index futures COB: 08:00 – 22:00  (call 07:30–08:00)
        SSF / dividend futures    : 09:01 – 17:30
    Modelled as 07:30 – 22:00 (widest — FTSE MIB futures).

    Milan is FULLY CLOSED on Christmas Eve (24 Dec) and New Year's Eve
    (31 Dec) — not a half day, unlike other Euronext markets.
    This is already correctly modelled in XMIL which this calendar inherits.

    Holidays: inherited from XMIL.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_MIL_INDEX", "ENX_FIB", "ENX_FTSEMIB"]
    _cash_cal = _xmil

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(22, 0)),),
    }

    @property
    def name(self):
        return "ENX_MIL_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Rome")


# ---------------------------------------------------------------------------
# 6. Euronext Oslo Derivatives
#    OBX Total Return Index Futures (OBF), Oslo Single Stock Futures (OF.)
#    OBX Index Options (OBX), Oslo Individual Equity Options (OO.)
#
#    COB: 09:01–16:20  (call phase 07:30–09:01)
#    Oslo is fully closed on Xmas Eve and NYE, and has a half-day
#    session on the Wednesday before Easter.
# ---------------------------------------------------------------------------

class EuronextOsloIndexDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Oslo Børs — Index & Equity Derivatives
    (OBX Total Return Futures OBF, Single Stock Futures OF.,
     OBX Index Options OBX, Individual Equity Options OO.)

    Normal session (CET/CEST):
        Call phase : 07:30 – 09:01
        COB        : 09:01 – 16:20
    Modelled as 07:30 – 16:20.

    Oslo-specific closures (additional vs core Euronext):
        - Maundy Thursday (Thu before Easter)
        - Ascension Day (39 days after Easter, always Thursday)
        - Whit Monday (49 days after Easter + 1)
        - Constitution Day (17 May)
        - Christmas Eve (24 Dec) — fully closed, not half day
        - New Year's Eve (31 Dec) — fully closed, not half day
    Half-trading-day:
        - Wednesday before Easter (Oslo Børs only)
    All inherited from XOSL.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_OSL_INDEX", "ENX_OBF", "ENX_OBX"]
    _cash_cal = _xosl

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(16, 20)),),
    }

    @property
    def name(self):
        return "ENX_OSL_INDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Oslo")


# ---------------------------------------------------------------------------
# 7. Euronext Paris Commodity Derivatives
#    Milling Wheat (YF.EBM/YO.OBM), Rapeseed (YF.ECO/YO.OCO),
#    Corn (YF.EMA/YO.OMA), European Durum Wheat (YF.EDW),
#    Salmon Futures (YF.ESF), Spread Futures (YF.BCS/BKS/BMS)
#
#    COB: 10:45–18:30  (call phase 07:30–10:45)
#    Salmon: 08:30–13:55
#    Modelled as 07:30–18:30 (widest window).
#    Same holiday set as XPAR.
# ---------------------------------------------------------------------------

class EuronextParisCommodityDerivsCalendar(_EuronextDerivsMixin, MarketCalendar):
    """
    Euronext Paris — Commodity Derivatives
    (Milling Wheat YF.EBM/YO.OBM, Rapeseed YF.ECO/YO.OCO,
     Corn YF.EMA/YO.OMA, Durum Wheat YF.EDW,
     Salmon YF.ESF, Spread Futures YF.BCS/BKS/BMS)

    Normal session (CET/CEST):
        Grains/oilseeds call phase : 07:30 – 10:45
        Grains/oilseeds COB        : 10:45 – 18:30
        Salmon COB                 : 08:30 – 13:55
    Modelled as 07:30 – 18:30 (grains/oilseeds widest window).

    Half-trading-day close: 14:05 CET (inherited from XPAR).
    Note: no expiries on half-trading days per Euronext rules.
    Holidays: inherited from XPAR.

    Source: https://live.euronext.com/en/media/295/download
    """

    aliases = ["ENX_PAR_COMM", "ENX_WHEAT", "ENX_AGRI"]
    _cash_cal = _xpar

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(18, 30)),),
    }

    @property
    def name(self):
        return "ENX_PAR_COMM"

    @property
    def tz(self):
        return ZoneInfo("Europe/Paris")