from datetime import time
from zoneinfo import ZoneInfo

import pandas as pd
from pandas.tseries.holiday import (
    AbstractHolidayCalendar,
    Holiday,
    GoodFriday,
    EasterMonday,
    weekend_to_monday,
    next_monday,
    next_monday_or_tuesday,
)
from pandas_market_calendars.market_calendar import MarketCalendar


# ---------------------------------------------------------------------------
# Shared holiday building blocks (unchanged)
# ---------------------------------------------------------------------------

_NewYearsDay = Holiday("New Year's Day", month=1, day=1, observance=weekend_to_monday)
_LabourDay1May = Holiday("Labour Day (1 May)", month=5, day=1, observance=weekend_to_monday)
_UKMayDay = Holiday("May Day Bank Holiday", month=5, day=1,
                    offset=pd.offsets.WeekOfMonth(week=0, weekday=0))
_UKSpringBankHoliday = Holiday("Spring Bank Holiday", month=5, day=1,
                                offset=pd.offsets.LastWeekOfMonth(weekday=0))
_UKSummerBankHoliday = Holiday("Summer Bank Holiday", month=8, day=1,
                                offset=pd.offsets.LastWeekOfMonth(weekday=0))
_ChristmasDay = Holiday("Christmas Day", month=12, day=25, observance=next_monday_or_tuesday)
_BoxingDay = Holiday("Boxing Day", month=12, day=26, observance=next_monday_or_tuesday)

_ADHOC_ALL = [
    pd.Timestamp("2022-06-03"),  # Platinum Jubilee
    pd.Timestamp("2022-09-19"),  # Queen Elizabeth II funeral
    pd.Timestamp("2023-05-08"),  # King Charles III coronation
]

# ---------------------------------------------------------------------------
# Early-close holiday rules
# ---------------------------------------------------------------------------

# Christmas Eve — 24 Dec, falls on a weekday (if Sat/Sun the day before
# the observed Christmas is used by ICE; in practice ICE publishes
# specific dates each year. This rule covers the standard case.)
_ChristmasEve = Holiday("Christmas Eve", month=12, day=24)
_NewYearsEve  = Holiday("New Year's Eve", month=12, day=31)

# US holidays that cause early closes on IFEU Energy (18:30 UK) and
# some other segments. These are the standard observed dates.
_MLKDay = Holiday("Martin Luther King Jr Day", month=1, day=1,
                  offset=pd.offsets.WeekOfMonth(week=2, weekday=0))
_PresidentsDay = Holiday("Presidents' Day", month=2, day=1,
                         offset=pd.offsets.WeekOfMonth(week=2, weekday=0))
_MemorialDay = Holiday("Memorial Day", month=5, day=1,
                       offset=pd.offsets.LastWeekOfMonth(weekday=0))
_Juneteenth = Holiday("Juneteenth", month=6, day=19, observance=weekend_to_monday)
_IndependenceDay = Holiday("Independence Day", month=7, day=4, observance=weekend_to_monday)
_LaborDay = Holiday("Labor Day", month=9, day=1,
                    offset=pd.offsets.WeekOfMonth(week=0, weekday=0))
_ThanksgivingDay = Holiday("Thanksgiving", month=11, day=1,
                           offset=pd.offsets.WeekOfMonth(week=3, weekday=3))
_ThanksgivingFriday = Holiday("Thanksgiving Friday", month=11, day=1,
                               offset=[pd.offsets.WeekOfMonth(week=3, weekday=3)
                               ,pd.offsets.Day(1)])


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------

class _IFEUBase(MarketCalendar):

    @property
    def tz(self):
        return ZoneInfo("Europe/London")

    @property
    def adhoc_holidays(self):
        return list(_ADHOC_ALL)


# ---------------------------------------------------------------------------
# 1. Energy  (Brent, WTI, Gasoil, Heating Oil, RBOB, Dubai …)
#
#    Regular hours: 01:00–23:00 London (near-24h; Sunday open 23:00 prev)
#    Full closes:   New Year's Day, Good Friday, Christmas Day
#    Early closes:
#      - Christmas Eve:        19:00 UK  (energy closes 19:00 per Appendix 1)
#      - New Year's Eve:       20:00 UK
#      - US holidays (C):      18:30 UK  (MLK, Presidents', Juneteenth,
#                                         Independence Day, Labor Day,
#                                         Thanksgiving Day)
#      - Thanksgiving Friday:  20:00 UK  (status B)
#      - Spring BH/Memorial Day: 18:30 UK (status D — same early close)
# ---------------------------------------------------------------------------

class IFEUEnergyExchangeCalendar(_IFEUBase):
    """
    ICE Futures Europe — Energy contracts
    (Brent, WTI, Midland WTI AGC, Permian WTI Storage, Low Sulphur Gasoil,
    Heating Oil, ULS Heating Oil, ULS Diesel, RBOB Gasoline, Dubai Crude)

    Regular session: 01:00–23:00 Europe/London
    Full closures:   New Year's Day, Good Friday, Christmas Day
    Early closes:
        19:00  Christmas Eve (24 Dec)
        20:00  New Year's Eve (31 Dec)
        18:30  US holidays: MLK Day, Presidents' Day, Memorial Day /
               Spring Bank Holiday, Juneteenth, Independence Day,
               Labor Day, Thanksgiving Day
        20:00  Thanksgiving Friday
    """

    aliases = ["IFEU_ENERGY"]

    @property
    def name(self):
        return "IFEU_ENERGY"

    regular_market_times = {
            "market_open":  ((None, time(1, 0)),),
            "market_close": ((None, time(23, 0)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            _ChristmasDay,
        ])

    @property
    def special_closes(self):
        return [
            (time(19, 0), AbstractHolidayCalendar(rules=[_ChristmasEve])),
            (time(20, 0), AbstractHolidayCalendar(rules=[
                _NewYearsEve,
                _ThanksgivingFriday,
            ])),
            (time(18, 30), AbstractHolidayCalendar(rules=[
                _MLKDay,
                _PresidentsDay,
                _MemorialDay,       # also Spring Bank Holiday — same date
                _Juneteenth,
                _IndependenceDay,
                _LaborDay,
                _ThanksgivingDay,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 2. UK Natural Gas, Power & Emissions
#
#    Regular hours: 07:00–17:00 London (UK Gas/Power/Emissions window)
#    Full closes:   All UK bank holidays
#    Early closes:
#      - Christmas Eve:   17:00 UK (UK Gas/Power/Emissions closes 17:00
#                                   per Christmas schedule)
#      - New Year's Eve:  17:00 UK (same — UK Gas closes 17:00 on NYE too)
#      NB: US holidays do not cause early closes for this segment.
# ---------------------------------------------------------------------------

class IFEUNaturalGasAndEmissionsExchangeCalendar(_IFEUBase):
    """
    ICE Futures Europe — UK Natural Gas, Power & Emissions
    (UK NBP Gas, UK Electricity, UK NBP Gas 1st Line, Dutch TTF 1st Line,
    French PEG, German THE, Italian PSV, NWE/SWE LNG,
    UKA Futures/Options, Global Carbon Index, Nature-Based Carbon, CORSIA)

    Regular session: 07:00–17:00 Europe/London
    Full closures:   All UK bank holidays
    Early closes:
        17:00  Christmas Eve (24 Dec)
        17:00  New Year's Eve (31 Dec)  [UK Gas/Power only; other
               contracts in this family may close later — see ICE circulars]
    """

    aliases = ["IFEU_GAS", "IFEU_EMISSIONS"]

    @property
    def name(self):
        return "IFEU_GAS"

    regular_market_times ={
            "market_open":  ((None, time(7, 0)),),
            "market_close": ((None, time(17, 0)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _UKMayDay,
            _UKSpringBankHoliday,
            _UKSummerBankHoliday,
            _ChristmasDay,
            _BoxingDay,
        ])

    @property
    def special_closes(self):
        return [
            (time(17, 0), AbstractHolidayCalendar(rules=[
                _ChristmasEve,
                _NewYearsEve,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 3. Soft Commodities / Agricultural
#    (London Cocoa, Robusta Coffee, White Sugar, UK Feed Wheat)
#
#    Regular hours: 08:45–17:30 London (conservative span across all softs)
#    Full closes:   All UK bank holidays
#    Early closes:
#      - Christmas Eve: 12:23 UK (softs close ~12:23 per ICE schedule;
#                                  Feed Wheat 12:18, others 12:23)
#      - New Year's Eve: softs trade normal hours on NYE (full day close
#                        times apply — Cocoa 16:55, Coffee 17:30,
#                        Sugar 18:00; modelled as normal close)
#      NB: NYE is a normal full trading day for softs per the 2025 schedule.
# ---------------------------------------------------------------------------

class IFEUSoftCommoditiesExchangeCalendar(_IFEUBase):
    """
    ICE Futures Europe — Soft Commodity / Agricultural contracts
    (London Cocoa, Robusta Coffee, White Sugar, UK Feed Wheat)

    Regular session: 08:45–17:30 Europe/London
    Full closures:   All UK bank holidays
    Early closes:
        12:23  Christmas Eve (24 Dec) — softs close ~12:23
               (Feed Wheat 12:18, Cocoa/Coffee/Sugar 12:23)
    New Year's Eve trades normal hours for softs.
    """

    aliases = ["IFEU_SOFTS", "IFEU_AGRI"]

    @property
    def name(self):
        return "IFEU_SOFTS"

    regular_market_times ={
            "market_open":  ((None, time(8, 45)),),
            "market_close": ((None, time(17, 30)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _UKMayDay,
            _UKSpringBankHoliday,
            _UKSummerBankHoliday,
            _ChristmasDay,
            _BoxingDay,
        ])

    @property
    def special_closes(self):
        return [
            (time(12, 23), AbstractHolidayCalendar(rules=[_ChristmasEve])),
        ]

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 4. UK Fixed Income & Rates
#    (Gilts, GBP SONIA Swapnote, 3M/1M SONIA, MPC Dated SONIA)
#
#    Regular hours: 08:00–18:00 London
#    Full closes:   All UK bank holidays + 1 May Labour Day
#    Early closes:
#      - Christmas Eve: 12:15 UK (Gilts/SONIA close 12:15 per schedule)
#      - New Year's Eve: 12:15 UK (same pattern as Christmas Eve)
# ---------------------------------------------------------------------------

class IFEUUKFixedIncomeExchangeCalendar(_IFEUBase):
    """
    ICE Futures Europe — UK Fixed Income & Rates
    (Short/Medium/Long/Ultra Long Gilts, Long Gilt Options,
    GBP SONIA Swapnote, 1M/3M SONIA Futures & Options, MPC Dated SONIA)

    Regular session: 08:00–18:00 Europe/London
    Full closures:   All UK bank holidays + Labour Day (1 May)
    Early closes:
        12:15  Christmas Eve (24 Dec)
        12:15  New Year's Eve (31 Dec)
    """

    aliases = ["IFEU_GILTS", "IFEU_SONIA"]

    @property
    def name(self):
        return "IFEU_GILTS"

    regular_market_times = {
        
            "market_open":  ((None, time(8, 0)),),
            "market_close": ((None, time(18, 0)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _LabourDay1May,
            _UKMayDay,
            _UKSpringBankHoliday,
            _UKSummerBankHoliday,
            _ChristmasDay,
            _BoxingDay,
        ])

    @property
    def special_closes(self):
        return [
            (time(12, 15), AbstractHolidayCalendar(rules=[
                _ChristmasEve,
                _NewYearsEve,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 5. European Fixed Income & Rates
#    (Bund, BTP, Bonos, OAT, CONF, Euribor, ESTR, SARON, Euro Swapnote)
#
#    Regular hours: 01:00–21:00 London (Euribor/Bund near-24h)
#    Full closes:   ECB set — New Year's Day, Good Friday, Easter Monday,
#                  Labour Day (1 May), Christmas Day
#    Early closes:
#      - Christmas Eve: 12:15 UK (all EUR FI closes 12:15 per schedule)
#      - New Year's Eve: 12:15 UK
#      - US holidays (SOFR Swapnote only — modelled separately if needed;
#        for the main EUR FI contracts no US holiday early close applies)
# ---------------------------------------------------------------------------

class IFEUEuropeanFixedIncomeExchangeCalendar(_IFEUBase):
    """
    ICE Futures Europe — European Fixed Income & Rates
    (Bund, BTP, Bonos, OAT, CONF, EU Bond Index,
    Euribor Futures & Options, 1M/3M ESTR, ECB Dated ESTR,
    SARON, Euro Swapnote)

    Regular session: 01:00–21:00 Europe/London
    Full closures:   New Year's Day, Good Friday, Easter Monday,
                     Labour Day (1 May), Christmas Day
    Early closes:
        12:15  Christmas Eve (24 Dec)
        12:15  New Year's Eve (31 Dec)
    Note: SOFR Swapnote & SOFR Index Futures have additional US holiday
    early closes (to 18:00/19:00 UK) — not modelled here as they are a
    USD-rate product that trades independently of the EUR FI close time.
    """

    aliases = ["IFEU_BUND", "IFEU_EURIBOR", "IFEU_EUR_FI"]

    @property
    def name(self):
        return "IFEU_EUR_FI"

    regular_market_times = {
            "market_open":  ((None, time(1, 0)),),
            "market_close": ((None, time(21, 0)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _LabourDay1May,
            _ChristmasDay,
        ])

    @property
    def special_closes(self):
        return [
            (time(12, 15), AbstractHolidayCalendar(rules=[
                _ChristmasEve,
                _NewYearsEve,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 6. UK Equity Derivatives
#    (FTSE 100/250 Futures & Options, UK Single Stocks, UK ETF Options)
#
#    Regular hours: 08:00–21:00 London (FTSE 100 futures near-continuous)
#    Full closes:   All UK bank holidays
#    Early closes:
#      - Christmas Eve: 12:50 UK (FTSE 100/250 futures close 12:50,
#                                  options 12:50 per 2025 schedule)
#      - New Year's Eve: 12:50 UK (same)
# ---------------------------------------------------------------------------

class IFEUEquityExchangeCalendar(_IFEUBase):
    """
    ICE Futures Europe — UK Equity Derivatives
    (FTSE 100 Index Futures & Options, Mini FTSE 100,
    FTSE 250 Futures & Options, FTSE 100 Total Return,
    FTSE 100 Dividend Index, FTSE 100 UK ESG,
    UK Single Stock Futures & Options, UK ETF Options)

    Regular session: 08:00–21:00 Europe/London
    Full closures:   All UK bank holidays
    Early closes:
        12:50  Christmas Eve (24 Dec)
        12:50  New Year's Eve (31 Dec)
    """

    aliases = ["IFEU_FTSE", "IFEU_EQUITY"]

    @property
    def name(self):
        return "IFEU_EQUITY"

    regular_market_times =  {
            "market_open":  ((None, time(8, 0)),),
            "market_close": ((None, time(21, 0)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _UKMayDay,
            _UKSpringBankHoliday,
            _UKSummerBankHoliday,
            _ChristmasDay,
            _BoxingDay,
        ])

    @property
    def special_closes(self):
        return [
            (time(12, 50), AbstractHolidayCalendar(rules=[
                _ChristmasEve,
                _NewYearsEve,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return []


# ---------------------------------------------------------------------------
# 7. ICE Endex
#    (TTF Gas, Power, EUAs, GOs — Amsterdam/CET)
#
#    Regular hours: 06:00–23:00 CET
#    Full closes:   New Year's Day, Good Friday, Easter Monday, Christmas Day
#    Early closes:
#      - US holidays (C): 19:30 CET early close for Gas/Power
#      - Thanksgiving Friday (B): 21:00 CET early close for Gas/Power
#      - Spring BH/Memorial Day (C): 19:30 CET
#
#    NB: CET = UTC+1 winter, CEST = UTC+2 summer. 
#    Christmas/NYE are in winter so GMT times from Appendix 1 map to CET
#    (GMT+1). e.g. 19:00 GMT Christmas Eve energy close = 20:00 CET.
#    The Endex schedule uses CET throughout; 14:00 CET = 13:00 GMT is
#    the key settlement anchor for the A-status days.
# ---------------------------------------------------------------------------

class ICEEndexGasPowerExchangeCalendar(MarketCalendar):
    """
    ICE Endex — Continental European Energy Derivatives
    (TTF Natural Gas Futures & Options, Power Futures & Options)

    Amsterdam-based; all times in CET/CEST (Europe/Amsterdam).

    Regular session: 06:00–23:00 CET
    Full closures:
        - New Year's Day
        - Good Friday
        - Easter Monday
        - Christmas Day (25 Dec)

    Early closes (CET):
        14:00  Christmas Eve (24 Dec)   — status A (early settlement)
        14:00  New Year's Eve (31 Dec)  — status A (early settlement)
        19:30  US holidays: MLK Day, Presidents' Day, Memorial Day /
               Spring Bank Holiday, Juneteenth, Independence Day,
               Labor Day, Thanksgiving Day  — status C
        21:00  Thanksgiving Friday      — status B

    Source: https://www.ice.com/publicdocs/ICE_Endex_Trading_Schedule.pdf
    """

    aliases = ["ENDEX", "ICE_ENDEX"]

    @property
    def name(self):
        return "ENDEX"

    @property
    def tz(self):
        return ZoneInfo("Europe/Amsterdam")

    regular_market_times=  {
            "market_open":  ((None, time(6, 0)),),
            "market_close": ((None, time(23, 0)),),
        }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _ChristmasDay,
        ])

    @property
    def adhoc_holidays(self):
        return list(_ADHOC_ALL)

    @property
    def special_closes(self):
        return [
            (time(19, 30), AbstractHolidayCalendar(rules=[
                _MLKDay,
                _PresidentsDay,
                _MemorialDay,
                _Juneteenth,
                _IndependenceDay,
                _LaborDay,
                _ThanksgivingDay,
            ])),
            (time(21, 0), AbstractHolidayCalendar(rules=[
                _ThanksgivingFriday,
            ])),
        ]

    @property
    def special_closes_adhoc(self):
        return []

class ICEEndexEmissionsExchangeCalendar(MarketCalendar):
    """
    ICE Endex — Emissions contracts
    (EUA Futures & Options, GO Futures)

    Amsterdam-based; all times in CET/CEST (Europe/Amsterdam).

    Regular session: 08:00–18:00 CET (EUA trading hours per contract spec)

    Full closures:
        - New Year's Day
        - Good Friday
        - Easter Monday
        - Christmas Day (25 Dec)

    No early closes — US holidays do not affect emissions contracts
    on Endex. Christmas Eve and New Year's Eve are status A (early
    settlement only, normal trading hours) so are not early closes.

    Source: https://www.ice.com/publicdocs/ICE_Endex_Trading_Schedule.pdf
    """

    aliases = ["ENDEX_EMISSIONS", "ENDEX_EUA"]

    @property
    def name(self):
        return "ENDEX_EMISSIONS"

    @property
    def tz(self):
        return ZoneInfo("Europe/Amsterdam")

    regular_market_times = {
        "market_open":  ((None, time(8, 0)),),
        "market_close": ((None, time(18, 0)),),
    }

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[
            _NewYearsDay,
            GoodFriday,
            EasterMonday,
            _ChristmasDay,
        ])

    @property
    def adhoc_holidays(self):
        return list(_ADHOC_ALL)

    @property
    def special_closes(self):
        return []

    @property
    def special_closes_adhoc(self):
        return []        