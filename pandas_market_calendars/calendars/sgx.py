"""
SGX Derivatives Exchange Calendars
====================================
Singapore Exchange (SGX) Derivatives Market.

Each contract family is a snowflake and has a different opening hours and
a different holiday closure set, combining:
  1. Singapore public holidays (the base for all SGX contracts)
  2. Reference market holidays for the underlying index/asset

Contracts covered and their holiday groups:

  SGX_CN  (NY only):
    CN    — FTSE China A50 Index Futures
    FCH   — FTSE China H50 Futures

  SGX_Singapore
  
  SGX_IronOre 
    FEF   — SGX IODEX Iron Ore (62% Fe) Futures
 
  SGX_Rubber (SG + NYE)
    TF    — SICOM Rubber (TSR20) Futures

  SGX_NK    (NY only):
    NK    — SGX Nikkei 225 Futures

  SGX_TWN   (NY only):
    TWN   — FTSE Taiwan RIC Capped (TWD) Index Futures

  SGX_NIFTY (Subset of NSE India holidays):
    NIFTY — SGX NSE IFSC Nifty 50 Index Futures

  SGX_IU    (NY only):
    IU    — SGX Indian Rupee in USD Futures

  SGX_KU    (NY only):
    KU    — SGX Korean Won in USD (Mini) Futures

  SGX_UC    (NY only)
    UC    — SGX USD/CNH Futures


Trading hours (SGT = Asia/Singapore = UTC+8, no DST):
  T session  : 08:30 – 17:30  (break-free continuous)
  T+1 session: 18:00 – 02:00  (next calendar day, SGT)
  The T+1 session is not modelled — library limitation.
  For FX contracts (UC): 07:00 – 18:00 (daytime only, different hours).
  For commodities (FEF, TF): 09:00 – 18:30.

Sources:
  SGX DT Trading Calendar 2025 (api2.sgx.com)
  SGX Rulebook Regulatory Notice 8.2.1
  tipranks.com Singapore exchange holiday lists 2024-2026
"""

from datetime import time
from zoneinfo import ZoneInfo

import pandas as pd
from pandas import Timestamp
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    Holiday,
    weekend_to_monday,
    previous_friday
)
from pandas.tseries.offsets import Day

from pandas_market_calendars.market_calendar import MarketCalendar


# ---------------------------------------------------------------------------
# Singapore public holidays
# ---------------------------------------------------------------------------

_SGNewYearsDay = Holiday(
    "New Year's Day", month=1, day=1, observance=weekend_to_monday
)

_SGNewYearsEve = Holiday(
    "New Year's Eve", month=12, day=31, observance=previous_friday
)

_SGLabourDay = Holiday(
    "Labour Day", month=5, day=1, observance=weekend_to_monday
)

_SGNationalDay = Holiday(
    "National Day", month=8, day=9, observance=weekend_to_monday
)

_SGChristmasDay = Holiday(
    "Christmas Day", month=12, day=25, observance=weekend_to_monday
)

# Lunar / Islamic Singapore holidays — ad-hoc because dates shift yearly.
# Covers 2020–2027. Source: MOM Singapore gazette + SGX trading calendars.
# Chinese New Year: 2 days
_SGChineseNewYear1 = [
    Timestamp("2020-01-25"), Timestamp("2021-02-12"), Timestamp("2022-02-01"),
    Timestamp("2023-01-23"), Timestamp("2024-02-10"), Timestamp("2025-01-29"),
    Timestamp("2026-02-17"), Timestamp("2027-02-06"),
]
_SGChineseNewYear2 = [
    Timestamp("2020-01-27"),  # Jan 26 Sun -> Mon Jan 27
    Timestamp("2021-02-13"), Timestamp("2022-02-02"),
    Timestamp("2023-01-24"), Timestamp("2024-02-12"),  # Feb 11 Sun -> Mon Feb 12
    Timestamp("2025-01-30"), Timestamp("2026-02-18"), Timestamp("2027-02-07"),
]

# Hari Raya Puasa (Eid al-Fitr)
_SGHariRayaPuasa = [
    Timestamp("2020-05-25"), Timestamp("2021-05-13"), Timestamp("2022-05-03"),
    Timestamp("2023-04-22"), Timestamp("2024-04-10"), Timestamp("2025-03-31"),
    # 2026: ~Mar 20 (Sat) -> observed Mon Mar 23
    Timestamp("2026-03-23"),
    Timestamp("2027-03-12"),
]

# Vesak Day
_SGVesakDay = [
    Timestamp("2020-05-07"), Timestamp("2021-05-26"), Timestamp("2022-05-15"),
    Timestamp("2023-06-02"),  # May 28 falls on Sun -> Mon 29? No, SG uses Jun 2 2023
    Timestamp("2024-05-22"), Timestamp("2025-05-12"),
    Timestamp("2026-06-01"),  # May 31 Sun -> Mon Jun 1
    Timestamp("2027-05-20"),
]

# Hari Raya Haji (Eid al-Adha)
_SGHariRayaHaji = [
    Timestamp("2020-07-31"), Timestamp("2021-07-20"), Timestamp("2022-07-10"),
    Timestamp("2023-06-29"), Timestamp("2024-06-17"), Timestamp("2025-06-06"),
    Timestamp("2026-05-27"), Timestamp("2027-05-17"),
]

# Deepavali
_SGDeepavali = [
    Timestamp("2020-11-14"), Timestamp("2021-11-04"), Timestamp("2022-10-24"),
    Timestamp("2023-11-13"), Timestamp("2024-10-31"), Timestamp("2025-10-20"),
    Timestamp("2026-11-09"),  # Nov 8 Sun -> Mon Nov 9
    Timestamp("2027-10-29"),
]

# All SG ad-hoc holidays combined
_SG_ADHOC = (
    _SGChineseNewYear1 + _SGChineseNewYear2
    + _SGHariRayaPuasa + _SGVesakDay
    + _SGHariRayaHaji + _SGDeepavali
)

# SGX early-close days: CNY Eve, Christmas Eve, New Year's Eve
# These are half-day sessions (close 12:30 SGT)
_SGCNYEveEarlyClose = [
    Timestamp("2020-01-24"), Timestamp("2021-02-11"), Timestamp("2022-01-31"),
    # 2023: Jan 21 is Sat — no market
    Timestamp("2024-02-08"), Timestamp("2025-01-28"), Timestamp("2026-02-16"),
    Timestamp("2027-02-05"),
]
_SGChristmasEve = Holiday("Christmas Eve", month=12, day=24)
_SGNewYearsEve = Holiday("New Year's Eve", month=12, day=31)



# ---------------------------------------------------------------------------
# NSE India holidays (for Gift NIFTY)
# Mostly ad-hoc 
# ---------------------------------------------------------------------------


_GIFTConnectHolidays = [
    Timestamp("2024-01-26"),  Timestamp("2024-10-02"),
    Timestamp("2026-01-26"), Timestamp("2026-10-02"), 
]

# ---------------------------------------------------------------------------
# India RBI/bank holidays (for IU — Indian Rupee futures)
# Smaller subset than NSE: Republic Day, Independence Day, Gandhi Jayanti,
# plus major religious holidays. Ad-hoc.
# ---------------------------------------------------------------------------

_RBIHolidays = [
    # Republic Day, Independence Day, Gandhi Jayanti (fixed, always observed)
    Timestamp("2020-01-26"), Timestamp("2020-08-15"), Timestamp("2020-10-02"),
    Timestamp("2021-01-26"), Timestamp("2021-08-15"), Timestamp("2021-10-02"),
    Timestamp("2022-01-26"), Timestamp("2022-08-15"), Timestamp("2022-10-02"),
    Timestamp("2023-01-26"), Timestamp("2023-08-15"), Timestamp("2023-10-02"),
    Timestamp("2024-01-26"), Timestamp("2024-08-15"), Timestamp("2024-10-02"),
    Timestamp("2025-01-26"), Timestamp("2025-08-15"), Timestamp("2025-10-02"),
    Timestamp("2026-01-26"), Timestamp("2026-08-15"), Timestamp("2026-10-02"),
    # Major religious/bank holidays (ad-hoc)
    Timestamp("2020-04-02"), Timestamp("2020-04-06"), Timestamp("2020-04-10"),
    Timestamp("2020-04-14"), Timestamp("2020-05-25"), Timestamp("2020-11-16"),
    Timestamp("2021-04-02"), Timestamp("2021-04-14"), Timestamp("2021-05-13"),
    Timestamp("2021-10-15"), Timestamp("2021-11-04"), Timestamp("2021-11-19"),
    Timestamp("2022-04-14"), Timestamp("2022-04-15"), Timestamp("2022-08-09"),
    Timestamp("2022-08-31"), Timestamp("2022-10-05"), Timestamp("2022-10-24"),
    Timestamp("2022-11-08"),
    Timestamp("2023-03-30"), Timestamp("2023-04-04"), Timestamp("2023-04-07"),
    Timestamp("2023-04-14"), Timestamp("2023-06-28"), Timestamp("2023-09-19"),
    Timestamp("2023-10-24"), Timestamp("2023-11-27"),
    Timestamp("2024-03-25"), Timestamp("2024-03-29"), Timestamp("2024-04-11"),
    Timestamp("2024-04-14"), Timestamp("2024-04-17"), Timestamp("2024-06-17"),
    Timestamp("2024-11-01"), Timestamp("2024-12-25"),
    Timestamp("2025-03-14"), Timestamp("2025-03-31"), Timestamp("2025-04-10"),
    Timestamp("2025-04-14"), Timestamp("2025-04-18"), Timestamp("2025-06-06"),
    Timestamp("2025-10-21"), Timestamp("2025-11-05"),
    Timestamp("2026-03-20"), Timestamp("2026-04-02"), Timestamp("2026-04-03"),
    Timestamp("2026-05-27"), Timestamp("2026-10-29"),
]


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class _SGXBase(MarketCalendar):
    """Internal base for SGX derivatives calendars."""

    @property
    def tz(self):
        return ZoneInfo("Asia/Singapore")


# ---------------------------------------------------------------------------
# 1. SGX Index — SG holidays only
#    Contracts: CN, SGP, FCH, UC, FEF, TF
# ---------------------------------------------------------------------------

class SGXIndexCNExchangeCalendar(_SGXBase):
    """
    A50 & H50 Futures 

    Closed only on Singapore public holidays.

    Regular session (SGT = UTC+8):
        T session  : 08:30 – 17:30
        T+1 session: 18:00 – 02:00 T+1

    Early closes (12:30 SGT):
        - CNY Eve (day before Chinese New Year Day 1)
        - Christmas Eve (24 Dec)
        - New Year's Eve (31 Dec)

    Source: SGX DT Trading Calendar 2025
    """

    aliases = ["SGX_CN"]

    regular_market_times = {
        "market_open":  ((None, time(9,0)),),
        "market_close": ((None, time(5, 15), 1),),   # T+1 session closes 05:15 T+1
        "break_start":  ((None, time(16, 30)),),   # T session closes 17:30
        "break_end":    ((None, time(16, 45)),),    # T+1 session opens 18:00
    }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
        ])

    @property
    def name(self):
        return "SGX_CN"


class SGXMSCISingaporeExchangeCalendar(_SGXBase):
    """
    Source: SGX DT Trading Calendar 2025
    """

    aliases = ["SGX_Singapore"]

    regular_market_times = {
        "market_open":  ((None, time(8,30)),),
        "market_close": ((None, time(5, 15)),),   # T+1 session closes 05:15 T+1
        "break_start":  ((None, time(17, 20)),),   # T session closes 17:30
        "break_end":    ((None, time(17, 35)),),    # T+1 session opens 18:00
    }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
        ])


    @property
    def name(self):
        return "SGX_Singapore"


class SGXIronOreExchangeCalendar(_SGXBase):
    aliases = ["SGX_IronOre"]

    regular_market_times = {
        "market_open":  ((None, time(7, 25)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(20, 0)),),   # T session closes 8pm
        "break_end":    ((None, time(20, 15)),),    # T+1 session opens 8:15pm
    }

    @property
    def name(self):
        return "SGX_IronOre"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
            _SGChristmasDay,
        ])


class SGXRubberExchangeCalendar(_SGXBase):
    aliases = ["SGX_Rubber"]


    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
            GoodFriday,
            _SGLabourDay,
            _SGNationalDay,
            _SGChristmasDay,
            _SGNewYearsEve,
        ])

    regular_market_times = {
        "market_open":  ((None, time(7, 55)),),
        "market_close": ((None, time(11, 0) ),),  
        "break_start":  ((None, time(18, 0)),),   # T session closes 6pm
        "break_end":    ((None, time(18, 15)),),    # T+1 session opens 6:15pm
    }

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC)


    @property
    def name(self):
        return "SGX_Rubber"


# ---------------------------------------------------------------------------
# 2. SGX NK — Nikkei 225
# ---------------------------------------------------------------------------

class SGXNikkeiExchangeCalendar(_SGXBase):
    """
    SGX — Nikkei 225 Futures (NK)

    Source: SGX DT Trading Calendar 2025
    """

    aliases = ["SGX_NK", "SGX_NIKKEI"]

    regular_market_times = {
        "market_open":  ((None, time(7, 30)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(15, 0)),),  
        "break_end":    ((None, time(15, 10)),),    # T+1 session opens 15:00
    }

    @property
    def name(self):
        return "SGX_NK"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
        ])



# ---------------------------------------------------------------------------
# 3. SGX TWN — FTSE Taiwan RIC Capped Futures
# ---------------------------------------------------------------------------

class SGXTaiwanExchangeCalendar(_SGXBase):
    """
    SGX — FTSE Taiwan RIC Capped (TWD) Index Futures (TWN)

    Source: SGX DT Trading Calendar 2025; TWSE holiday announcements.
    """

    aliases = ["SGX_TWN", "SGX_TAIWAN"]

    regular_market_times = {
        "market_open":  ((None, time(8, 45)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(13, 45)),),   
        "break_end":    ((None, time(13, 0)),),    # T+1 session opens 14:00
    }

    @property
    def name(self):
        return "SGX_TWN"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay, 
        ])


# ---------------------------------------------------------------------------
# 4. SGX NIFTY — SGX NSE IFSC Nifty 50 Index Futures
# ---------------------------------------------------------------------------

class SGXNiftyExchangeCalendar(_SGXBase):
    """
    SGX — SGX NSE IFSC Nifty 50 Index Futures (NIFTY)

    Closed only on some indian holidays, and not every year.

    Regular session: 09:00 – 18:10 SGT (NSE session proxy).

    Source: SGX DT Trading Calendar 2024-2026;
    """

    aliases = ["SGX_NIFTY"]

    regular_market_times = {
        "market_open":  ((None, time(9, 0)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(18, 10)),),   
        "break_end":    ((None, time(18, 35)),),    # T+1 session opens 18:35
    }

    @property
    def name(self):
        return "SGX_NIFTY"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[])

    @property
    def adhoc_holidays(self):
        return _GIFTConnectHolidays


# ---------------------------------------------------------------------------
# 5. SGX IU — SGX Indian Rupee in USD Futures
# ---------------------------------------------------------------------------

class SGXIndianRupeeExchangeCalendar(_SGXBase):
    """
    SGX — SGX Indian Rupee in USD Futures (IU)

    Source: SGX DT Trading Calendar 2025; RBI holiday notices.
    """

    aliases = ["SGX_IU", "SGX_INR"]

    regular_market_times = {
        "market_open":  ((None, time(7, 25)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(19, 30)),),   # T session closes 17:30
        "break_end":    ((None, time(19, 50)),),    # T+1 session opens 18:00
    }

    @property
    def name(self):
        return "SGX_IU"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay, 
        ])



# ---------------------------------------------------------------------------
# 6. SGX KU — SGX Korean Won in USD (Mini) Futures
# ---------------------------------------------------------------------------

class SGXKoreanWonExchangeCalendar(_SGXBase):
    """
    SGX — SGX Korean Won in USD (Mini) Futures (KU)

    Source: SGX DT Trading Calendar 2025; 
    """

    aliases = ["SGX_KU", "SGX_KRW"]

    regular_market_times = {
        "market_open":  ((None, time(7, 25)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(19, 30)),),   # T session closes 19:30
        "break_end":    ((None, time(19, 50)),),    # T+1 session opens 19:50
    }

    @property
    def name(self):
        return "SGX_KU"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
        ])


    

class SGXCNHExchangeCalendar(_SGXBase):
    aliases = ["SGX_UC", "SGX_CNH"]

    regular_market_times = {
        "market_open":  ((None, time(7, 25)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(18, 0)),),   # T session closes 18:00
        "break_end":    ((None, time(18, 15)),),    # T+1 session opens 18:15
    }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
        ])

    @property
    def name(self):
        return "SGX_UC"