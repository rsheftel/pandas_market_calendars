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
from typing import Any, List
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

from pandas_market_calendars.market_calendar import MONDAY, TUESDAY
from pandas_market_calendars.holidays.us import (
    Christmas as USChristmas,
    USIndependenceDay,
    USJuneteenthAfter2022,
    USMartinLutherKingJrAfter1998,
    USMemorialDay,
    USNationalDaysofMourning,
    USJuneteenthAfter2022,
    USNewYearsDay,
    ChristmasEveInOrAfter1993 as USChristmasEve,
    USNewYearsEve
)
from pandas_market_calendars.holidays.ca import (
    RemembranceDay,
    TruthAndReconciliationDay,
    VictoriaDay,
    CanadaDay,
    LaborDay,
    CivicHoliday,
    Christmas,
    Thanksgiving,
    FamilyDay,
    NewYears,
)
from pandas_market_calendars.holidays.uk import (
    Christmas as UKChristmas, BoxingDay, WeekendChristmas, WeekendBoxingDay
)
from pandas_market_calendars.market_calendar import MarketCalendar


CanolaWeekendBoxingDay1 = Holiday(
    name="Canola Weekend Boxing Day", month=12, day=27, days_of_week=(MONDAY, TUESDAY)
)
CanolaWeekendBoxingDay2 = Holiday(
    name="Canola Weekend Boxing Day", month=12, day=28, days_of_week=(MONDAY,)
)

# ---------------------------------------------------------------------------
# Shared adhoc closures (national days of mourning etc.)
# ---------------------------------------------------------------------------
_ADHOC = list(
    chain(
        USNationalDaysofMourning,
        [Timestamp("2012-10-29", tz="UTC")],  # Hurricane Sandy
    )
)


class ICEExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for ICE US 

    Open Time: 8pm, US/Eastern
    Close Time: 6pm, US/Eastern

    https://www.theice.com/publicdocs/futures_us/ICE_Futures_US_Regular_Trading_Hours.pdf # noqa
    """
    # FIXME: This is legacy and wrong in many ways - I dont think this should be used any more.

    aliases = ["ICE", "ICEUS", "NYFE"]
    regular_market_times = {
        "market_open": ((None, time(20, 1), -1),),  # offset by -1 day
        "market_close": ((None, time(18)),),
    }

    @property
    def name(self) -> str:
        return "ICE"

    @property
    def tz(self) -> Any:
        return ZoneInfo("US/Eastern")

    @property
    def special_closes(self) -> List[Any]:
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
    def adhoc_holidays(self) -> List[Any]:
        return list(
            chain(
                USNationalDaysofMourning,
                # ICE was only closed on the first day of the Hurricane Sandy
                # closings (was not closed on 2012-10-30)
                [Timestamp("2012-10-29", tz="UTC")],
            )
        )

    @property
    def regular_holidays(self) -> Any:
        # https://www.theice.com/publicdocs/futures_us/exchange_notices/NewExNot2016Holidays.pdf
        return AbstractHolidayCalendar(rules=[USNewYearsDay, GoodFriday, Christmas])


class ICEUSSoftsBaseCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Soft Commodity Contracts
    
    Closed on ALL standard US holidays:
        New Year's Day, MLK Day, Presidents' Day, Good Friday,
        Memorial Day, Juneteenth, Independence Day,
        Labor Day, Thanksgiving Day, Christmas Day.
    """
    
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


class ICEUSCoffeeCalendar(ICEUSSoftsBaseCalendar):
    """
    ICE Futures U.S. — Cofee
    (Coffee "C"®, Coffee "C"® Metric)

    Trading hours (ET, sessions start previous business day):
        04:15 – 13:30 ET

    Around DST changes the opening hours move with UK timezone,
    but we don't have the tools to model that here.
    """

    aliases = ["ICEUS_COFFEE"]

    regular_market_times = {
        "market_open": ((None, time(4, 15)),),
        "market_close": ((None, time(13, 30)),),
    }

    @property
    def name(self):
        return "ICEUS_COFFEE"
    
    @property
    def special_closes(self):
        return [
            (time(13,5), AbstractHolidayCalendar(rules=[USChristmasEve]),)
        ]

class ICEUSCottonCalendar(ICEUSSoftsBaseCalendar):
    """
    ICE Futures U.S. — Cotton
    (Cotton No. 2)

    Trading hours (ET, sessions start previous business day):
        21:00 (T-1) – 14:20 ET

    Occasionally there is a late start for Cotton post holidays but we haven't
    got tools to model that here.
    """

    aliases = ["ICEUS_COTTON"]

    regular_market_times = {
        "market_open": ((None, time(21, 0), -1),),
        "market_close": ((None, time(14, 20)),),
    }

    @property
    def name(self):
        return "ICEUS_COTTON"

    @property
    def special_closes(self):
        return [
            (time(13,5), AbstractHolidayCalendar(rules=[USChristmasEve]),)
        ]

class ICEUSCocoaCalendar(ICEUSSoftsBaseCalendar):
    """
    ICE Futures U.S. — Cocoa

    Trading hours (ET, sessions start previous business day):
        04:45 – 13:30 ET

    Around DST changes the opening hours move with UK timezone,
    but we don't have the tools to model that here. Occasionally 
    there is a late start post holidays but we haven't got tools 
    to model that here.
    """

    aliases = ["ICEUS_COCOA"]

    regular_market_times = {
        "market_open": ((None, time(4, 45)),),
        "market_close": ((None, time(13, 30)),),
    }

    @property
    def name(self):
        return "ICEUS_COCOA"

    @property
    def special_closes(self):
        return [
            (time(13,5), AbstractHolidayCalendar(rules=[USChristmasEve]),)
        ]

class ICEUSSugar11Calendar(ICEUSSoftsBaseCalendar):
    """
    ICE Futures U.S. — Sugar No. 11

    Trading hours (ET, sessions start previous business day):
        03:30 – 13:00 ET

    Around DST changes the opening hours move with UK timezone,
    but we don't have the tools to model that here. Occasionally 
    there is a late start post holidays but we haven't got tools 
    to model that here.
    """

    aliases = ["ICEUS_SUGAR11"]

    regular_market_times = {
        "market_open": ((None, time(3, 30)),),
        "market_close": ((None, time(13, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_SUGAR11"

class ICEUSSugar16Calendar(ICEUSSoftsBaseCalendar):
    """
    ICE Futures U.S. — Sugar No. 16

    Trading hours (ET, sessions start previous business day):
        09:00 – 13:00 ET
    """

    aliases = ["ICEUS_SUGAR16"]

    regular_market_times = {
        "market_open": ((None, time(9, 0)),),
        "market_close": ((None, time(13, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_SUGAR16"



class ICEUSCanolaCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Canola Futures 

    Follows Canadian public holidays (plus the following):
        - National Day for Truth and Reconciliation (30 Sep)
        - Remembrance Day (11 Nov)

    Canadian holidays observed:
        New Year's Day, Louis Riel Day / Family day (3rd Mon Feb),
        Good Friday, Victoria Day (Mon before May 25),
        Canada Day (1 Jul), Terry Fox Day / Civic Holiday (1st Mon Aug),
        Labour Day (1st Mon Sep), National Day for Truth & Reconciliation
        (30 Sep), Thanksgiving Canada (2nd Mon Oct),
        Remembrance Day (11 Nov), Christmas, Boxing Day.

    Weekend christmases are treated a bit funny - saturday christmas results in
    Fri,Mon holidays, unlike Canada convention of Mon,Tue. (or US convention of 
    just Fri)

    Trading hours:
        20:00 T-1 – 14:20 ET

    Occasionally there is a late start post holidays, but we don't have tools to
    model that.

    """

    aliases = ["ICEUS_CANOLA"]

    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(14, 20)),),
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
                CanadaDay,
                CivicHoliday,
                LaborDay,
                TruthAndReconciliationDay,
                Thanksgiving,
                RemembranceDay,
                USChristmas,
                BoxingDay,
                CanolaWeekendBoxingDay1,
                CanolaWeekendBoxingDay2,
            ]
        )

    @property
    def adhoc_holidays(self):
        # Probably are some but don't know RN
        return []

    @property
    def special_closes(self):
        return [
            (time(13,5), AbstractHolidayCalendar(rules=[USChristmasEve]),)
        ]

    @property
    def special_closes_adhoc(self):
        return []



class ICEUSEnergiesCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Energies Contracts
    (Nat Gas, Power, Enviornmental, Oil)

    NB: The source says boxing day early close, but the notices 
    typically say christmas eve early close.

    Normal trading hours: 19:50 T-1 – 18:00 ET 
    """

    aliases = ["ICEUS_ENERGIES"]

    regular_market_times = {
        "market_open": ((None, time(19, 50), -1),),
        "market_close": ((None, time(18, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_ENERGIES"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def regular_holidays(self):
        # Only New Year's Day and Christmas
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                GoodFriday,
                USChristmas,
            ]
        )

    @property
    def adhoc_holidays(self):
        return list(_ADHOC)

    @property
    def special_closes(self):
        return [
            (
                time(13, 30),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        USMemorialDay,
                        USJuneteenthAfter2022,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                        USChristmasEve,
                        BoxingDay
                    ]
                ),
            )
        ]

    @property
    def special_closes_adhoc(self):
        return []



class ICEUSFxCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Financial Contracts
    (US Dollar Index® (DX), Currency pairs)

    Closed ONLY on New Year's Day and Christmas Day.
    Open on all other US holidays  — with per-holiday modified hours 
    published via advance Exchange Notice. Those modified hours
    change the closing time and choice of holidays each year, so
    we just model it as 13:30 (which is approximately correct)

    NB: The source says boxing day early close, but the notices 
    typically say christmas eve early close.

    Normal trading hours (ET):
        DX / Currency Pairs      : 20:00* – 17:00 ET (* prev business day)
    """

    aliases = ["ICEUS_DX", "ICEUS_FX"]

    regular_market_times = {
        # 20:00 ET previous business day open, 17:00 ET close
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(17, 0)),),
    }

    @property
    def name(self):
        return "ICEUS_FX"

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
        return [
            (
                time(13, 30),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        GoodFriday,
                        USMemorialDay,
                        USJuneteenthAfter2022,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                        USChristmasEve,
                    ]
                ),
            )
        ]

    @property
    def special_closes_adhoc(self):
        return []



class ICEUSFinancialsCalendar(MarketCalendar):
    """
    Exchange calendar for ICE US Financials
    (MSCI, FTSE and NYSE Stock Index Futures, ICE Mortgage Index Futures,
    MSCI Corporate Bond Index Futures, Digital Asset Futures)

    Open Time: 8pm, US/Eastern T-1
    Close Time: 6pm, US/Eastern

    Opens earlier on a sunday but noone trades that, and half day closes vary in their times, 
    but 13:30 is first order correct. [13:00 - 14:30 is the range]
    """

    aliases = ["ICEUS_FINANCIALS"]  
    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),  # offset by -1 day
        "market_close": ((None, time(18)),),
    }

    @property
    def name(self):
        return "ICEUS_FINANCIALS"

    @property
    def tz(self):
        return ZoneInfo("US/Eastern")

    @property
    def special_closes(self):
        return [
            (
                time(13, 30),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        GoodFriday,
                        USMemorialDay,
                        USJuneteenthAfter2022,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                        USChristmasEve,
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
        return AbstractHolidayCalendar(rules=[USNewYearsDay, USChristmas])



class ICEUSDailyGoldSilverCalendar(MarketCalendar):
    """
    ICE Futures U.S. — Daily Gold and Silver Contracts

    Full closures:
        New Year's Day, Good Friday, Memorial Day,
        Christmas Day, Boxing Day.

    Follows UK Christmas/Boxing day conventions.

    Note: Daily Gold and Silver contracts may also be closed on LBMA
    holidays not listed here — details published via Exchange Notice.
    Open (with per-notice modified hours) on MLK, Presidents, Juneteenth,
    Independence Day, Labor Day, Thanksgiving.

    Half day close times vary with holiday & year. Have just modelled as 1330 
    for now.

    Trading hours (ET): 20:00* – 18:00 ET (* prev business day).
    """

    aliases = ["ICE_DAILY_PR", "ICEUS_DAILY_AU", "ICEUS_DAILY_AG"]

    regular_market_times = {
        "market_open": ((None, time(20, 0), -1),),
        "market_close": ((None, time(18, 0)),),
    }

    @property
    def name(self):
        return "ICE_DAILY_PR"

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
                UKChristmas,
                BoxingDay,
                WeekendChristmas,
                WeekendBoxingDay                ,
            ]
        )


    @property
    def special_closes(self):
        return [
            (
                time(13, 30),
                AbstractHolidayCalendar(
                    rules=[
                        USMartinLutherKingJrAfter1998,
                        USPresidentsDay,
                        USJuneteenthAfter2022,
                        USIndependenceDay,
                        USLaborDay,
                        USThanksgivingDay,
                        USChristmasEve,
                    ]
                ),
            )
        ]
    @property
    def special_closes_adhoc(self):
        return []
