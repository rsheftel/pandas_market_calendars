"""
SGX Derivatives Exchange Calendars
====================================
Singapore Exchange (SGX) Derivatives Market.

Each contract family is a snowflake and has a different opening hours and
a different holiday closure set, combining:
  1. Singapore public holidays (the base for all SGX contracts)
  2. Reference market holidays for the underlying index/asset

Contracts covered and their holiday groups:

  SGX_Index  (SG holidays only):
    CN    — FTSE China A50 Index Futures
    SGP   — MSCI Singapore Index Futures
    FCH   — FTSE China H50 Futures

  
  SGX_IronOre
    FEF   — SGX IODEX Iron Ore (62% Fe) Futures
 
  SGX_Rubber (SG + NYE)
    TF    — SICOM Rubber (TSR20) Futures

  SGX_NK    (SG + Japan holidays):
    NK    — SGX Nikkei 225 Futures

  SGX_TWN   (SG + Taiwan Stock Exchange holidays):
    TWN   — FTSE Taiwan RIC Capped (TWD) Index Futures

  SGX_NIFTY (SG + NSE India holidays):
    NIFTY — SGX NSE IFSC Nifty 50 Index Futures

  SGX_IU    (SG + India RBI/bank holidays — a subset of NSE):
    IU    — SGX Indian Rupee in USD Futures

  SGX_KU    (SG + Korean holidays):
    KU    — SGX Korean Won in USD (Mini) Futures

  SGX_UC
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
# Japan public holidays (for NK — Nikkei 225)
# Fixed-date holidays with observance rules + ad-hoc equinoxes
# ---------------------------------------------------------------------------

def _jp_observed(dt):
    """Japan substitute holiday: if holiday falls on Sunday, next Monday off.
    If Monday is also a holiday, Tuesday is off (sandwiched day rule — not
    fully implemented here; most cases are covered by the Sunday->Monday shift).
    """
    if dt.weekday() == 6:  # Sunday
        return dt + Day(1)
    return dt

_JPNewYearsDay = Holiday("JP New Year's Day", month=1, day=1, observance=_jp_observed)
_JPComingOfAgeDay = Holiday(
    "Coming of Age Day", month=1, day=1,
    offset=pd.offsets.WeekOfMonth(week=1, weekday=0)  # 2nd Monday of Jan
)
_JPNationalFoundationDay = Holiday(
    "National Foundation Day", month=2, day=11, observance=_jp_observed
)
_JPEmperorBirthday = Holiday(
    "Emperor's Birthday", month=2, day=23, observance=_jp_observed
)
_JPShowaDay = Holiday("Showa Day", month=4, day=29, observance=_jp_observed)
_JPConstitutionDay = Holiday("Constitution Day", month=5, day=3, observance=_jp_observed)
_JPGreeneryDay = Holiday("Greenery Day", month=5, day=4, observance=_jp_observed)
_JPChildrensDay = Holiday("Children's Day", month=5, day=5, observance=_jp_observed)
_JPMarineDay = Holiday(
    "Marine Day", month=7, day=1,
    offset=pd.offsets.WeekOfMonth(week=2, weekday=0)  # 3rd Monday of Jul
)
_JPMountainDay = Holiday("Mountain Day", month=8, day=11, observance=_jp_observed)
_JPRespectForAgedDay = Holiday(
    "Respect for the Aged Day", month=9, day=1,
    offset=pd.offsets.WeekOfMonth(week=2, weekday=0)  # 3rd Monday of Sep
)
_JPSportsDay = Holiday(
    "Sports Day", month=10, day=1,
    offset=pd.offsets.WeekOfMonth(week=1, weekday=0)  # 2nd Monday of Oct
)
_JPCultureDay = Holiday("Culture Day", month=11, day=3, observance=_jp_observed)
_JPLabourThanksgivingDay = Holiday(
    "Labour Thanksgiving Day", month=11, day=23, observance=_jp_observed
)

# Vernal and Autumnal Equinox: date varies ~Mar 20 and ~Sep 23; ad-hoc needed
_JPVernalEquinox = [
    Timestamp("2020-03-20"), Timestamp("2021-03-20"), Timestamp("2022-03-21"),
    Timestamp("2023-03-21"), Timestamp("2024-03-20"), Timestamp("2025-03-20"),
    Timestamp("2026-03-20"), Timestamp("2027-03-21"),
]
_JPAutumnalEquinox = [
    Timestamp("2020-09-22"), Timestamp("2021-09-23"), Timestamp("2022-09-23"),
    Timestamp("2023-09-23"), Timestamp("2024-09-22"), Timestamp("2025-09-23"),
    Timestamp("2026-09-23"), Timestamp("2027-09-23"),
]
# Japan year-end / New Year: exchange closed Dec 31 – Jan 3
# Jan 2-3 are not public holidays but TSE/SGX NK does not trade them.
_JPYearEndNewYear = [
    Timestamp("2020-01-02"), Timestamp("2020-01-03"), Timestamp("2020-12-31"),
    Timestamp("2021-01-02"), Timestamp("2021-01-03"), Timestamp("2021-12-31"),
    Timestamp("2022-01-02"), Timestamp("2022-01-03"), Timestamp("2022-12-31"),  # Dec 31 Sat
    Timestamp("2023-01-02"), Timestamp("2023-01-03"), Timestamp("2023-12-31"),
    Timestamp("2024-01-02"), Timestamp("2024-01-03"), Timestamp("2024-12-31"),
    Timestamp("2025-01-02"), Timestamp("2025-01-03"), Timestamp("2025-12-31"),
    Timestamp("2026-01-02"), Timestamp("2026-01-03"), Timestamp("2026-12-31"),
    Timestamp("2027-01-02"), Timestamp("2027-01-03"), Timestamp("2027-12-31"),
]
# Substitute "sandwich" days (between two holidays) — ad-hoc
_JPSubstituteDays = [
    Timestamp("2020-09-21"),  # Mon between Sun equinox and Respect for Aged
    Timestamp("2021-08-09"),  # Mountain Day moved for Olympics
    Timestamp("2021-07-22"),  # Marine Day moved for Olympics
    Timestamp("2021-07-23"),  # Sports Day moved for Olympics
    Timestamp("2024-09-20"),  # Substitute/bridge day
]

_JP_ADHOC = _JPVernalEquinox + _JPAutumnalEquinox + _JPYearEndNewYear + _JPSubstituteDays


# ---------------------------------------------------------------------------
# Taiwan Stock Exchange holidays (for TWN)
# Mix of fixed and lunar/ad-hoc
# ---------------------------------------------------------------------------

_TWNewYearsDay = Holiday("TW New Year's Day", month=1, day=1, observance=_jp_observed)
_TWPeaceMemorialDay = Holiday(
    "Peace Memorial Day", month=2, day=28, observance=_jp_observed
)
_TWChildrensDay = Holiday("Children's Day", month=4, day=4, observance=_jp_observed)
_TWNationalDay = Holiday("National Day", month=10, day=10, observance=_jp_observed)

# Lunar holidays for Taiwan — ad-hoc, 2020–2027
# Chinese New Year (Taiwan typically closes 3-5 days around CNY)
_TWLunarHolidays = [
    # 2020: Jan 23-29 (Thu-Wed, CNY Jan 25)
    Timestamp("2020-01-23"), Timestamp("2020-01-24"), Timestamp("2020-01-27"),
    Timestamp("2020-01-28"), Timestamp("2020-01-29"),
    # 2021: Feb 10-16 (Wed-Tue, CNY Feb 12)
    Timestamp("2021-02-10"), Timestamp("2021-02-11"), Timestamp("2021-02-15"),
    Timestamp("2021-02-16"),
    # 2022: Jan 31-Feb 4 (Mon-Fri, CNY Feb 1)
    Timestamp("2022-01-31"), Timestamp("2022-02-02"), Timestamp("2022-02-03"),
    Timestamp("2022-02-04"),
    # 2023: Jan 20-27 (Fri-Fri, CNY Jan 22)
    Timestamp("2023-01-20"), Timestamp("2023-01-23"), Timestamp("2023-01-24"),
    Timestamp("2023-01-25"), Timestamp("2023-01-26"), Timestamp("2023-01-27"),
    # 2024: Feb 8-14 (Thu-Wed, CNY Feb 10)
    Timestamp("2024-02-08"), Timestamp("2024-02-09"), Timestamp("2024-02-13"),
    Timestamp("2024-02-14"),
    # 2025: Jan 27-Feb 4 (Mon-Tue, CNY Jan 29)
    Timestamp("2025-01-27"), Timestamp("2025-01-28"), Timestamp("2025-01-29"),
    Timestamp("2025-01-30"), Timestamp("2025-01-31"),
    # 2026: Feb 16-20 (Mon-Fri, CNY Feb 17)
    Timestamp("2026-02-16"), Timestamp("2026-02-19"), Timestamp("2026-02-20"),
    # 2027: Feb 5-9 (Fri-Tue, CNY Feb 6)
    Timestamp("2027-02-05"), Timestamp("2027-02-08"), Timestamp("2027-02-09"),
]
# Tomb Sweeping Day (Ching Ming) Taiwan — typically Apr 4 or Apr 5
_TWTombSweeping = [
    Timestamp("2020-04-02"), Timestamp("2020-04-03"),  # bridge + Ching Ming
    Timestamp("2021-04-02"), Timestamp("2021-04-05"),
    Timestamp("2022-04-04"), Timestamp("2022-04-05"),
    Timestamp("2023-04-03"), Timestamp("2023-04-04"), Timestamp("2023-04-05"),
    Timestamp("2024-04-04"), Timestamp("2024-04-05"),
    Timestamp("2025-04-03"), Timestamp("2025-04-04"),
    Timestamp("2026-04-03"), Timestamp("2026-04-06"),
    Timestamp("2027-04-05"),
]
# Dragon Boat Festival (Taiwan)
_TWDragonBoat = [
    Timestamp("2020-06-25"), Timestamp("2020-06-26"),
    Timestamp("2021-06-14"),
    Timestamp("2022-06-03"),
    Timestamp("2023-06-22"), Timestamp("2023-06-23"),
    Timestamp("2024-06-10"),
    Timestamp("2025-05-30"), Timestamp("2025-05-31"),
    Timestamp("2026-06-19"), Timestamp("2026-06-20"),
    Timestamp("2027-06-08"), Timestamp("2027-06-09"),
]
# Mid-Autumn Festival (Taiwan)
_TWMidAutumn = [
    Timestamp("2020-10-01"), Timestamp("2020-10-02"),
    Timestamp("2021-09-20"), Timestamp("2021-09-21"),
    Timestamp("2022-09-09"),
    Timestamp("2023-09-29"),
    Timestamp("2024-09-17"),
    Timestamp("2025-10-06"),
    Timestamp("2026-09-25"),
    Timestamp("2027-09-15"),
]

_TW_ADHOC = _TWLunarHolidays + _TWTombSweeping + _TWDragonBoat + _TWMidAutumn


# ---------------------------------------------------------------------------
# NSE India holidays (for NIFTY)
# Mostly ad-hoc — NSE publishes the list annually
# ---------------------------------------------------------------------------

_NSEHolidays = [
    # 2020
    Timestamp("2020-02-21"), Timestamp("2020-03-10"), Timestamp("2020-04-02"),
    Timestamp("2020-04-06"), Timestamp("2020-04-10"), Timestamp("2020-04-14"),
    Timestamp("2020-05-01"), Timestamp("2020-05-25"), Timestamp("2020-10-02"),
    Timestamp("2020-11-16"), Timestamp("2020-11-30"),
    # 2021
    Timestamp("2021-01-26"), Timestamp("2021-03-11"), Timestamp("2021-03-29"),
    Timestamp("2021-04-02"), Timestamp("2021-04-14"), Timestamp("2021-04-21"),
    Timestamp("2021-05-13"), Timestamp("2021-07-21"), Timestamp("2021-08-19"),
    Timestamp("2021-09-10"), Timestamp("2021-10-15"), Timestamp("2021-11-04"),
    Timestamp("2021-11-05"), Timestamp("2021-11-19"),
    # 2022
    Timestamp("2022-01-26"), Timestamp("2022-03-01"), Timestamp("2022-03-18"),
    Timestamp("2022-04-14"), Timestamp("2022-04-15"), Timestamp("2022-05-03"),
    Timestamp("2022-08-09"), Timestamp("2022-08-15"), Timestamp("2022-08-31"),
    Timestamp("2022-10-02"), Timestamp("2022-10-05"), Timestamp("2022-10-24"),
    Timestamp("2022-10-26"), Timestamp("2022-11-08"),
    # 2023
    Timestamp("2023-01-26"), Timestamp("2023-03-07"), Timestamp("2023-03-30"),
    Timestamp("2023-04-04"), Timestamp("2023-04-07"), Timestamp("2023-04-14"),
    Timestamp("2023-04-22"), Timestamp("2023-05-01"), Timestamp("2023-06-28"),
    Timestamp("2023-08-15"), Timestamp("2023-09-19"), Timestamp("2023-10-02"),
    Timestamp("2023-10-24"), Timestamp("2023-11-14"), Timestamp("2023-11-27"),
    Timestamp("2023-12-25"),
    # 2024
    Timestamp("2024-01-22"), Timestamp("2024-01-26"), Timestamp("2024-03-25"),
    Timestamp("2024-03-29"), Timestamp("2024-04-11"), Timestamp("2024-04-14"),
    Timestamp("2024-04-17"), Timestamp("2024-04-21"), Timestamp("2024-05-23"),
    Timestamp("2024-06-17"), Timestamp("2024-07-17"), Timestamp("2024-08-15"),
    Timestamp("2024-10-02"), Timestamp("2024-10-14"), Timestamp("2024-11-01"),
    Timestamp("2024-11-15"), Timestamp("2024-12-25"),
    # 2025
    Timestamp("2025-01-26"), Timestamp("2025-02-26"), Timestamp("2025-03-14"),
    Timestamp("2025-03-31"), Timestamp("2025-04-10"), Timestamp("2025-04-14"),
    Timestamp("2025-04-18"), Timestamp("2025-05-01"), Timestamp("2025-06-06"),
    Timestamp("2025-08-15"), Timestamp("2025-08-27"), Timestamp("2025-10-02"),
    Timestamp("2025-10-02"), Timestamp("2025-10-21"), Timestamp("2025-10-22"),
    Timestamp("2025-11-05"), Timestamp("2025-12-25"),
    # 2026 (approximate — verify against NSE announcement when published)
    Timestamp("2026-01-26"), Timestamp("2026-03-03"), Timestamp("2026-03-20"),
    Timestamp("2026-04-02"), Timestamp("2026-04-03"), Timestamp("2026-04-14"),
    Timestamp("2026-05-01"), Timestamp("2026-05-27"), Timestamp("2026-08-15"),
    Timestamp("2026-10-02"), Timestamp("2026-10-29"), Timestamp("2026-11-24"),
    Timestamp("2026-12-25"),
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
# Korean public holidays (for KU — Korean Won futures)
# Fixed + lunar ad-hoc
# ---------------------------------------------------------------------------

_KRFixedHolidays = [
    # Samil (Independence Movement) Day — Mar 1
    # Children's Day — May 5
    # Memorial Day — Jun 6
    # Liberation Day — Aug 15
    # National Foundation Day — Oct 3
    # Hangeul Day — Oct 9
    # Christmas — Dec 25
]

_KRSamil = Holiday("Samil Day", month=3, day=1, observance=_jp_observed)
_KRChildrensDay = Holiday("Children's Day", month=5, day=5, observance=_jp_observed)
_KRMemorialDay = Holiday("Memorial Day", month=6, day=6, observance=_jp_observed)
_KRLiberationDay = Holiday("Liberation Day", month=8, day=15, observance=_jp_observed)
_KRNationalFoundationDay = Holiday(
    "National Foundation Day", month=10, day=3, observance=_jp_observed
)
_KRHangeulDay = Holiday("Hangeul Day", month=10, day=9, observance=_jp_observed)
_KRChristmas = Holiday("Christmas", month=12, day=25, observance=_jp_observed)

# Lunar holidays: Seollal (LNY) 3 days, Chuseok (Harvest) 3 days,
# Buddha's Birthday — all ad-hoc
_KRLunarHolidays = [
    # 2020: Seollal Jan 24-27, Chuseok Sep 30-Oct 2, Buddha May 30
    Timestamp("2020-01-24"), Timestamp("2020-01-27"),
    Timestamp("2020-04-30"),  # substitute
    Timestamp("2020-09-30"), Timestamp("2020-10-01"), Timestamp("2020-10-02"),
    # 2021: Seollal Feb 11-13, Chuseok Sep 20-22, Buddha May 19
    Timestamp("2021-02-11"), Timestamp("2021-02-12"), Timestamp("2021-02-13"),
    Timestamp("2021-05-19"),
    Timestamp("2021-09-20"), Timestamp("2021-09-21"), Timestamp("2021-09-22"),
    # 2022: Seollal Feb 1-3, Chuseok Sep 9-12, Buddha May 8
    Timestamp("2022-02-01"), Timestamp("2022-02-02"), Timestamp("2022-02-03"),
    Timestamp("2022-05-08"), Timestamp("2022-05-10"),  # substitute
    Timestamp("2022-09-09"), Timestamp("2022-09-12"),
    # 2023: Seollal Jan 21-24, Chuseok Sep 28-Oct 3, Buddha May 29
    Timestamp("2023-01-21"), Timestamp("2023-01-23"), Timestamp("2023-01-24"),
    Timestamp("2023-05-29"),
    Timestamp("2023-09-28"), Timestamp("2023-09-29"), Timestamp("2023-10-02"),
    # 2024: Seollal Feb 9-12, Chuseok Sep 16-18, Buddha May 15
    Timestamp("2024-02-09"), Timestamp("2024-02-12"),
    Timestamp("2024-05-15"),
    Timestamp("2024-09-16"), Timestamp("2024-09-17"), Timestamp("2024-09-18"),
    # 2025: Seollal Jan 28-30, Chuseok Oct 5-7, Buddha May 5
    Timestamp("2025-01-28"), Timestamp("2025-01-29"), Timestamp("2025-01-30"),
    Timestamp("2025-10-05"), Timestamp("2025-10-06"), Timestamp("2025-10-07"),
    # 2026: Seollal Feb 16-18, Chuseok Sep 24-26, Buddha May 24
    Timestamp("2026-02-16"),Timestamp("2026-02-17"), Timestamp("2026-02-18"), 
    Timestamp("2026-05-25"),  # May 24 Sun -> Mon
    Timestamp("2026-09-24"), Timestamp("2026-09-25"), Timestamp("2026-09-28"),
    # 2027: Seollal Feb 6-8, Chuseok Sep 14-16, Buddha May 13
    Timestamp("2027-02-06"), Timestamp("2027-02-07"), Timestamp("2027-02-08"),
    Timestamp("2027-05-13"),
    Timestamp("2027-09-14"), Timestamp("2027-09-15"), Timestamp("2027-09-16"),
]
# Korea year-end: KRX closed Dec 31 most years
_KRYearEnd = [
    Timestamp("2020-12-31"), Timestamp("2021-12-31"),
    Timestamp("2022-12-30"),  # Dec 31 Sat
    Timestamp("2023-12-29"),  # Dec 31 Sun -> but KRX closes the last trading day
    Timestamp("2024-12-31"), Timestamp("2025-12-31"),
    Timestamp("2026-12-31"), Timestamp("2027-12-31"),
]

_KR_ADHOC = _KRLunarHolidays + _KRYearEnd


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class _SGXBase(MarketCalendar):
    """Internal base for SGX derivatives calendars."""

    @property
    def tz(self):
        return ZoneInfo("Asia/Singapore")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay,
            GoodFriday,
            _SGLabourDay,
            _SGNationalDay,
            _SGChristmasDay,
        ])

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC)

    @property
    def special_closes(self):
        # Half-day sessions (close 12:30 SGT)
        return [
            (time(12, 30), AbstractHolidayCalendar(rules=[
                _SGChristmasEve,
                _SGNewYearsEve,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return [(time(12, 30), _SGCNYEveEarlyClose)]


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
    def name(self):
        return "SGX_CN"


class SGXMSCISingaporeExchangeCalendar(_SGXBase):
    """
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

    aliases = ["SGX_Singapore"]

    regular_market_times = {
        "market_open":  ((None, time(8,30)),),
        "market_close": ((None, time(5, 15)),),   # T+1 session closes 05:15 T+1
        "break_start":  ((None, time(17, 20)),),   # T session closes 17:30
        "break_end":    ((None, time(17, 35)),),    # T+1 session opens 18:00
    }

    @property
    def name(self):
        return "SGX"


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
    def name(self):
        return "SGX_Rubber"


# ---------------------------------------------------------------------------
# 2. SGX NK — Nikkei 225
# ---------------------------------------------------------------------------

class SGXNikkeiExchangeCalendar(_SGXBase):
    """
    SGX — Nikkei 225 Futures (NK)

    Closed on Singapore public holidays AND Japan national holidays.
    Also closed Jan 2-3 and Dec 31 (Japan year-end convention).

    Regular session (SGT = UTC+8): 07:30 – 14:30 (JST session proxy)
    Modelled as standard SGX equity hours 08:30 – 17:30 for simplicity.

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
        sg_rules = [
            _SGNewYearsDay, GoodFriday, _SGLabourDay,
            _SGNationalDay, _SGChristmasDay,
        ]
        jp_rules = [
            _JPNewYearsDay, _JPComingOfAgeDay, _JPNationalFoundationDay,
            _JPEmperorBirthday, _JPShowaDay, _JPConstitutionDay,
            _JPGreeneryDay, _JPChildrensDay, _JPMarineDay, _JPMountainDay,
            _JPRespectForAgedDay, _JPSportsDay, _JPCultureDay,
            _JPLabourThanksgivingDay,
        ]
        return AbstractHolidayCalendar(rules=sg_rules + jp_rules)

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC) + _JP_ADHOC


# ---------------------------------------------------------------------------
# 3. SGX TWN — FTSE Taiwan RIC Capped Futures
# ---------------------------------------------------------------------------

class SGXTaiwanExchangeCalendar(_SGXBase):
    """
    SGX — FTSE Taiwan RIC Capped (TWD) Index Futures (TWN)

    Closed on Singapore public holidays AND Taiwan Stock Exchange holidays.

    Regular session: 08:45 – 13:45 SGT (TWSE morning session proxy).
    Modelled as 08:30 – 17:30 for consistency with other SGX contracts.

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
            _SGNewYearsDay, GoodFriday, _SGLabourDay,
            _SGNationalDay, _SGChristmasDay,
            _TWNewYearsDay, _TWPeaceMemorialDay,
            _TWChildrensDay, _TWNationalDay,
        ])

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC) + _TW_ADHOC


# ---------------------------------------------------------------------------
# 4. SGX NIFTY — SGX NSE IFSC Nifty 50 Index Futures
# ---------------------------------------------------------------------------

class SGXNiftyExchangeCalendar(_SGXBase):
    """
    SGX — SGX NSE IFSC Nifty 50 Index Futures (NIFTY)

    Closed on Singapore public holidays AND NSE India holidays.
    NSE holidays are gazetted annually and must be updated each year.

    Regular session: 09:00 – 18:30 SGT (NSE session proxy).
    Modelled as 08:30 – 17:30 for consistency.

    NB: 2026 NSE holidays are approximate — verify against official NSE
    announcement when published.

    Source: SGX DT Trading Calendar 2025; NSE India holiday lists.
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
        return AbstractHolidayCalendar(rules=[
            _SGNewYearsDay, GoodFriday, _SGLabourDay,
            _SGNationalDay, _SGChristmasDay,
        ])

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC) + _NSEHolidays


# ---------------------------------------------------------------------------
# 5. SGX IU — SGX Indian Rupee in USD Futures
# ---------------------------------------------------------------------------

class SGXIndianRupeeExchangeCalendar(_SGXBase):
    """
    SGX — SGX Indian Rupee in USD Futures (IU)

    Closed on Singapore public holidays AND India RBI/bank holidays.
    The RBI holiday set is a subset of the full NSE holiday list,
    covering Republic Day, Independence Day, Gandhi Jayanti, and
    major religious holidays.

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
            _SGNewYearsDay, GoodFriday, _SGLabourDay,
            _SGNationalDay, _SGChristmasDay,
        ])

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC) + _RBIHolidays


# ---------------------------------------------------------------------------
# 6. SGX KU — SGX Korean Won in USD (Mini) Futures
# ---------------------------------------------------------------------------

class SGXKoreanWonExchangeCalendar(_SGXBase):
    """
    SGX — SGX Korean Won in USD (Mini) Futures (KU)

    Closed on Singapore public holidays AND South Korean public holidays.
    KRX also closes on Dec 31 (last trading day convention).

    Regular session: 07:30 – 18:00 SGT (FX hours).
    Modelled as 08:30 – 17:30 for consistency.

    Source: SGX DT Trading Calendar 2025; KRX holiday announcements.
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
            _SGNewYearsDay, GoodFriday, _SGLabourDay,
            _SGNationalDay, _SGChristmasDay,
            _KRSamil, _KRChildrensDay, _KRMemorialDay,
            _KRLiberationDay, _KRNationalFoundationDay,
            _KRHangeulDay, _KRChristmas,
        ])

    @property
    def adhoc_holidays(self):
        return list(_SG_ADHOC) + _KR_ADHOC

    

class SGXCNHExchangeCalendar(_SGXBase):
    aliases = ["SGX_UC", "SGX_CNH"]

    regular_market_times = {
        "market_open":  ((None, time(7, 25)),),
        "market_close": ((None, time(5, 15), 1),),  # T+1 session closes 05:15 SGT next day
        "break_start":  ((None, time(18, 0)),),   # T session closes 18:00
        "break_end":    ((None, time(18, 15)),),    # T+1 session opens 18:15
    }

    @property
    def name(self):
        return "SGX_UC"