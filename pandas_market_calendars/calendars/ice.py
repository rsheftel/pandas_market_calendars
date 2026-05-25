"""
ICE Futures U.S. (ICEUS) Exchange Calendars
=============================================
Replaces / extends the existing ice.py ICEExchangeCalendar which uses a single
calendar for all ICEUS products. That is incorrect: ICEUS has two fundamentally
different holiday regimes depending on product group.

Per the 2026 IFUS Trading Holiday Calendar and Regular Trading Hours documents:
  https://www.ice.com/publicdocs/futures/IFUS_Trading_Hours_Holiday_Calendar.pdf
  https://www.ice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf

Two calendars are provided:

  ICEUSSoftsCalendar
    Cocoa, Coffee "C"®, Cotton No.2®, FCOJ-A, Sugar No.11®, Sugar No.16
    Closed on ALL standard US holidays including Good Friday.

  ICEUSFinancialsCalendar
    US Dollar Index® (DX), Currency Pairs,
    NYSE Stock Index, MSCI Stock/Bond Index, FTSE Index,
    SOFR Index, ICE Mortgage Index, Digital Assets
    Closed ONLY on New Year's Day and Christmas Day.
    Open (possibly with minor modified hours per advance Exchange Notice)
    on all other US holidays including Good Friday.

Canola is NOT included — it follows Canadian holidays (a separate calendar).

Known issue with the existing ICEExchangeCalendar:
  - Incorrectly closes on Good Friday for ALL products (DX should be open)
  - Incorrectly shows MLK/Presidents as early-close rather than full closure
    for softs
  - Missing Juneteenth as a softs closure

All times are US/Eastern.

Sources:
  https://www.ice.com/publicdocs/futures/IFUS_Trading_Hours_Holiday_Calendar.pdf
  https://www.ice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf
"""

from datetime import time
from itertools import chain
from zoneinfo import ZoneInfo

from pandas import Timestamp
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    GoodFriday,
    Holiday,
    USLaborDay,
    USPresidentsDay,
    USThanksgivingDay,
    next_monday_or_tuesday,
)

from pandas_market_calendars.holidays.us import (
    Christmas as USChristmas,
    USIndependenceDay,
    USJuneteenthAfter2022,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNationalDaysofMourning,
    USNewYearsDay,
)
from pandas_market_calendars.holidays.ca import (
    RemembranceDay,
    TruthAndReconiliationDay,
    VictoriaDay,
    LaborDay,
    CivicHoliday,
    Christmas,
    Thanksgiving,
    FamilyDay,
    NewYears,
)
from pandas_market_calendars.holidays.uk import BoxingDay
from pandas_market_calendars.market_calendar import MarketCalendar


# ---------------------------------------------------------------------------
# Shared adhoc closures (national days of mourning etc.)
# ---------------------------------------------------------------------------
_ADHOC = list(
    chain(
        USNationalDaysofMourning,
        [Timestamp("2012-10-29", tz="UTC")],  # Hurricane Sandy
    )
)


# ---------------------------------------------------------------------------
# 1. ICE US Softs Calendar
#    Cocoa, Coffee "C", Cotton No.2, FCOJ-A, Sugar No.11, Sugar No.16
# ---------------------------------------------------------------------------


class ICEUSSoftsCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Soft Commodity Contracts
    (Cocoa, Coffee "C"®, Coffee "C"® Metric,
     Cotton No.2®, FCOJ-A,
     Sugar No.11®, Sugar No.16)

    Closed on ALL standard US holidays:
        New Year's Day, MLK Day, Presidents' Day, Good Friday,
        Memorial Day, Juneteenth, Independence Day,
        Labor Day, Thanksgiving Day, Christmas Day.

    Trading hours (ET, sessions start previous business day):
        Sugar No.11  : 03:30 – 13:00 ET
        Coffee "C"   : 04:15 – 13:30 ET
        Cotton No.2  : 21:00* – 14:20 ET   (* prev business day)
        FCOJ-A       : 08:00 – 14:00 ET
        Cocoa        : 08:00 – 14:00 ET
        Sugar No.16  : 19:45* – 17:00 ET   (* prev business day)
    Modelled as the widest daytime window: 03:30 – 17:00 ET.
    For per-contract precision, split into sub-calendars.

    Source:
        https://www.ice.com/publicdocs/futures/IFUS_Trading_Hours_Holiday_Calendar.pdf
        https://www.ice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf
    """

    aliases = ["ICEUS_SOFTS", "ICEUS_COCOA", "ICEUS_COFFEE", "ICEUS_COTTON", "ICEUS_SUGAR"]

    regular_market_times = {
        # Widest window covering all softs contracts
        # Sugar 11 opens earliest at 03:30 ET; Sugar 16 closes latest at 17:00 ET
        "market_open": ((None, time(3, 30)),),
        "market_close": ((None, time(17, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_SOFTS"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                USMartinLutherKingJrAfter1998,
                USPresidentsDay,
                GoodFriday,
                USMemorialDay,
                USJuneteenthAfter2022,
                USIndependenceDay,
                USLaborDay,
                USThanksgivingDay,
                USChristmas,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(_ADHOC)

    @property
    def special_closes(self):
        return []

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 2. ICE US Financials Calendar
#    DX, Currency Pairs, Stock/Bond Index, SOFR, Mortgage, Digital Assets
# ---------------------------------------------------------------------------


class ICEUSFinancialsCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Financial Contracts
    (US Dollar Index® (DX), Currency Pairs,
     NYSE Stock Index Futures, MSCI Stock/Bond Index Futures,
     FTSE Index Futures, SOFR Index Futures,
     ICE Mortgage Index Futures, Digital Asset Futures)

    Closed ONLY on New Year's Day and Christmas Day.
    Open on all other US holidays (MLK Day, Presidents' Day, Good Friday,
    Memorial Day, Juneteenth, Independence Day, Labor Day, Thanksgiving)
    — with per-holiday modified hours published via advance Exchange Notice.
    Those minor intra-day adjustments are not modelled here.

    Normal trading hours (ET):
        DX / Currency Pairs      : 20:00* – 17:00 ET (* prev business day)
        Stock/Bond/SOFR/Mortgage : 20:00* – 18:00 ET (* prev business day;
                                    Sunday open 18:00 ET)
    Modelled as the DX window: 20:00 ET prev day – 17:00 ET.

    Note: The existing ICEExchangeCalendar (ice.py) incorrectly closes this
    group on Good Friday and shows incorrect early-close behaviour on MLK,
    Presidents Day etc. This calendar corrects those errors.

    Source:
        https://www.ice.com/publicdocs/futures/IFUS_Trading_Hours_Holiday_Calendar.pdf
        https://www.ice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf
    """

    aliases = ["ICEUS_DX", "ICEUS_FX", "ICEUS_FINANCIALS"]

    regular_market_times = {
        # 20:00 ET previous business day open, 17:00 ET close
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(17, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_DX"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def regular_holidays(self):
        # Only New Year's Day and Christmas
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                USChristmas,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(_ADHOC)

    @property
    def special_closes(self):
        return []

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 3. ICE US Canola Calendar
# ---------------------------------------------------------------------------


# Pre-compute extra canola-specific holiday dates (TSX stays open, canola closes)


class ICEUSCanolaCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Canola Futures & Options

    Follows Canadian public holidays (plus the following):
        - National Day for Truth and Reconciliation (30 Sep)
        - Remembrance Day (11 Nov)

    Canadian holidays observed:
        New Year's Day, Louis Riel Day / Presidents Day / Family day (3rd Mon Feb),
        Good Friday, Victoria Day (Mon before May 25),
        Canada Day (1 Jul), Terry Fox Day / Civic Holiday (1st Mon Aug),
        Labour Day (1st Mon Sep), National Day for Truth & Reconciliation
        (30 Sep), Thanksgiving Canada (2nd Mon Oct),
        Remembrance Day (11 Nov), Christmas, Boxing Day.

    US holidays NOT observed (canola stays open):
        MLK Day, Memorial Day, Juneteenth, Independence Day,
        Thanksgiving (US), Columbus Day, Veterans Day.

    Trading hours (ET, daytime session only — no overnight):
        09:00 – 13:00 ET

    Source:
        https://www.ice.com/publicdocs/futures/IFUS_Trading_Hours_Holiday_Calendar.pdf
    """

    aliases = ["ICEUS_CANOLA"]

    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(13, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_CANOLA"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                NewYears,
                FamilyDay,
                GoodFriday,
                VictoriaDay,
                CivicHoliday,
                LaborDay,
                TruthAndReconiliationDay,
                Thanksgiving,
                RemembranceDay,
                Christmas,
                BoxingDay,
            ]
        )

    @property
    def adhoc_holidays(self):
        # Probably are some but don't know RN
        return []

    @property
    def special_closes(self):
        return []

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 4. ICE US Energy & Environmental Calendar
#    Financial Natural Gas, Oil, Power, NGL contracts
# ---------------------------------------------------------------------------


class ICEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for ICE US Energies

    Open Time: 8pm, US/Eastern
    Close Time: 6pm, US/Eastern

    Opens earlier on a sunday but noone trades that...

    https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf # noqa
    """

    aliases = ["ICE", "ICEUS", "NYFE", "ICEUS_ENERGY"]  # NYFE feels wrong here, but kept for legacy...
    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),  # offset by -1 day
        "market_close": ((None, time(18)),),
    }

    @property
    def name(self):
        return "ICE"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def special_closes(self):
        return [
            (
                time(13),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        USMemorialDay,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                    ]
                ),
            )
        ]

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                USNationalDaysofMourning,
                # ICE was only closed on the first day of the Hurricane Sandy
                # closings (was not closed on 2012-10-30)
                [Timestamp("2012-10-29", tz="UTC")],
            )
        )

    @property
    def regular_holidays(self):
        # https://www.theice.com/publicdocs/futures_us/exchange_notices/NewExNot2016Holidays.pdf
        return AbstractHolidayCalendar(rules=[USNewYearsDay, GoodFriday, USChristmas])


# ---------------------------------------------------------------------------
# 5. ICE US Daily Gold & Silver Calendar
# ---------------------------------------------------------------------------


class ICEUSDailyGoldSilverCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Daily Gold and Silver Contracts

    Differs from Energy on Memorial Day (Gold/Silver closed, Energy open)
    and Boxing Day (Gold/Silver closed, Energy open^1).

    Full closures:
        New Year's Day, Good Friday, Memorial Day,
        Christmas Day, Boxing Day (observed).

    Note: Daily Gold and Silver contracts may also be closed on LBMA
    holidays not listed here — details published via Exchange Notice.
    Open (with per-notice modified hours) on MLK, Presidents, Juneteenth,
    Independence Day, Labor Day, Thanksgiving.

    Trading hours (ET): 20:00* – 18:00 ET (* prev business day).

    Source:
        https://www.ice.com/publicdocs/futures/IFUS_Trading_Hours_Holiday_Calendar.pdf
    """

    aliases = ["ICEUS_GOLD", "ICEUS_SILVER"]

    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(18, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_GOLD"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                GoodFriday,
                USMemorialDay,
                USChristmas,
                # Boxing Day observed — Mon Dec 28 2026 (Dec 26 Sat -> Mon 28)
                # Use next_monday_or_tuesday observance on Dec 26
                Holiday("Boxing Day", month=12, day=26, observance=next_monday_or_tuesday),
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(_ADHOC)

    @property
    def special_closes(self):
        return []

    @property
    def special_closes_adhoc(self):
        return []
