from datetime import time
from itertools import chain

from pandas.tseries.holiday import AbstractHolidayCalendar
from zoneinfo import ZoneInfo

from pandas_market_calendars.holidays.jp import *
from pandas_market_calendars.holidays.us import USNewYearsDay
from pandas_market_calendars.market_calendar import MarketCalendar


# TODO:
# From 1949 to 1972 the TSE was open on all non-holiday Saturdays for a half day
# From 1973 to 1984 the TSE was open on all non-holiday Saturdays except the third Saturday of the month
# need to add support for weekmask to make this work properly


class JPXExchangeCalendar(MarketCalendar):
    """
    Exchange calendar for JPX

    Open Time: 9:31 AM, Asia/Tokyo
    LUNCH BREAK :facepalm: : 11:30 AM - 12:30 PM Asia/Tokyo
    Close Time: 3:30 PM, Asia/Tokyo

    Market close of Japan changed from 3:00 PM to 3:30 PM on November 5, 2024
    Reference:
    https://www.jpx.co.jp/english/equities/trading/domestic/tvdivq0000006blj-att/tradinghours_eg.pdf
    """

    aliases = ["JPX", "XJPX"]
    regular_market_times = {
        "market_open": ((None, time(9)),),
        "market_close": ((None, time(15)), ("2024-11-05", time(15, 30))),
        "break_start": ((None, time(11, 30)),),
        "break_end": ((None, time(12, 30)),),
    }
    regular_early_close = time(13)

    @property
    def name(self):
        return "JPX"

    @property
    def full_name(self):
        return "Japan Exchange Group"

    @property
    def tz(self):
        return ZoneInfo("Asia/Tokyo")

    @property
    def adhoc_holidays(self):
        return list(
            chain(
                AscensionDays,
                MarriageDays,
                FuneralShowa,
                EnthronementDays,
                AutumnalCitizenDates,
                NoN225IndexPrices,
                EquityTradingSystemFailure,
            )
        )

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(
            rules=[
                USNewYearsDay,
                JapanNewYearsDay2,
                JapanNewYearsDay3,
                JapanComingOfAgeDay1951To1973,
                JapanComingOfAgeDay1974To1999,
                JapanComingOfAgeDay,
                JapanNationalFoundationDay1969To1973,
                JapanNationalFoundationDay,
                JapanEmperorsBirthday,
                JapanVernalEquinox,
                JapanShowaDayUntil1972,
                JapanShowaDay,
                JapanConstitutionMemorialDayUntil1972,
                JapanConstitutionMemorialDay,
                JapanGreeneryDay,
                JapanChildrensDayUntil1972,
                JapanChildrensDay,
                JapanGoldenWeekBonusDay,
                JapanMarineDay1996To2002,
                JapanMarineDay2003To2019,
                JapanMarineDay2020,
                JapanMarineDay2021,
                JapanMarineDay,
                JapanMountainDay2016to2019,
                JapanMountainDay2020,
                JapanMountainDay2021,
                JapanMountainDay2021NextDay,
                JapanMountainDay,
                JapanRespectForTheAgedDay1966To1972,
                JapanRespectForTheAgedDay1973To2002,
                JapanRespectForTheAgedDay,
                JapanAutumnalEquinox,
                JapanHealthAndSportsDay1966To1972,
                JapanHealthAndSportsDay1973To1999,
                JapanHealthAndSportsDay2000To2019,
                JapanSportsDay2020,
                JapanSportsDay2021,
                JapanSportsDay,
                JapanCultureDayUntil1972,
                JapanCultureDay,
                JapanLaborThanksgivingDayUntil1972,
                JapanLaborThanksgivingDay,
                JapanEmperorAkahitosBirthday,
                JapanDecember29Until1988,
                JapanDecember30Until1988,
                JapanBeforeNewYearsDay,
            ]
        )


# ---------------------------------------------------------------------------
# OSE (Osaka Exchange) Derivatives Calendars
# Appended here as OSE is JPX's derivatives arm, sharing the same holiday set.
#
# Sessions (JST = Asia/Tokyo = UTC+9, no DST):
#
#   Index futures (Nikkei 225, TOPIX, JPX-Nikkei 400, etc.):
#     Day session  : 08:45 – 15:45 JST
#     Night session: 17:00 – 06:00 JST (next calendar day)
#     Modelled as: open=08:45, break_start=15:45, break_end=17:00,
#                  close=06:00+1 (next day offset)
#
#   JGB Futures / Interest Rate Futures:
#     Day morning  : 08:45 – 11:02 JST
#     Day afternoon: 12:30 – 15:02 JST
#     Night session: 15:30 – 06:00 JST (next calendar day)
#     The two-part day session cannot be fully modelled (one break supported).
#     Modelled conservatively as: open=08:45, break_start=15:02,
#                                  break_end=15:30, close=06:00+1
#
#   Note: The night session is cancelled when the following day is a holiday.
#   This is not modelled here — the library does not support conditional sessions.
#
# Source: https://www.jpx.co.jp/english/derivatives/rules/trading-hours/index.html
# ---------------------------------------------------------------------------


class OSEIndexFuturesCalendar(JPXExchangeCalendar):
    """
    Osaka Exchange (OSE) — Equity Index Futures & Options
    (Nikkei 225 Futures / Mini / Micro, TOPIX Futures / mini-TOPIX,
     JPX-Nikkei 400 Futures, TOPIX Core30, TOPIX Banks Index,
     TSE REIT Index, RN Prime Index, DJIA Futures,
     India Nifty50 Futures, FTSE China 50 Index Futures,
     Nikkei 225 / TOPIX Dividend Index Futures,
     Nikkei 225 Options / Weekly Options)

    Inherits all JPX holidays. Overrides trading hours for the futures
    day + night session structure (no lunch break).

    Day session  (JST): 08:45 – 15:45
    Night session (JST): 17:00 – 06:00 next day
    Modelled as: open=08:45, break_start=15:45, break_end=17:00, close=06:00+1.

    Night session is cancelled when the following calendar day is a holiday
    — this is not modelled (library limitation).

    Source: https://www.jpx.co.jp/english/derivatives/rules/trading-hours/index.html
    """

    aliases = ["OSE", "OSE_INDEX", "OSE_NK225", "OSE_TOPIX"]

    regular_market_times = {
        "market_open": ((None, time(8, 45)),),
        "market_close": ((None, time(6, 0), 1),),  # 06:00 JST next calendar day
        "break_start": ((None, time(15, 45)),),  # end of day session
        "break_end": ((None, time(17, 0)),),  # start of night session
    }

    @property
    def name(self):
        return "OSE"


class OSEJGBFuturesCalendar(JPXExchangeCalendar):
    """
    Osaka Exchange (OSE) — JGB Futures & Interest Rate Futures
    (10-Year JGB Futures, 5-Year JGB Futures, 3-Year JGB Futures,
     20-Year JGB Futures, Options on 10-Year JGB Futures,
     Euroyen TIBOR Futures, TONA Futures)

    Inherits all JPX holidays. Overrides trading hours for the JGB
    futures session structure.

    Day session has a morning and afternoon component:
        Morning  : 08:45 – 11:02 JST
        Afternoon: 12:30 – 15:02 JST
    Night session: 15:30 – 06:00 JST next day

    Only one break is supported by the library. Modelled as:
        open=08:45, break_start=15:02, break_end=15:30, close=06:00+1.
    The lunch break (11:02–12:30) is not modelled.

    Source: https://www.jpx.co.jp/english/derivatives/rules/trading-hours/index.html
    """

    aliases = ["OSE_JGB", "OSE_BOND"]

    regular_market_times = {
        "market_open": ((None, time(8, 45)),),
        "market_close": ((None, time(6, 0), 1),),  # 06:00 JST next calendar day
        "break_start": ((None, time(15, 2)),),  # end of afternoon day session
        "break_end": ((None, time(15, 30)),),  # start of night session
    }

    @property
    def name(self):
        return "OSE_JGB"


class OSEPreciousMetalsFuturesCalendar(JPXExchangeCalendar):
    """
    Osaka Exchange (OSE) — Precious Metals Futures & Options
    (Gold Standard Futures, Gold Mini Futures, Gold Rolling-Spot Futures,
     Options on Gold Futures, Pocket Gold 100 Futures,
     Silver Futures,
     Platinum Standard Futures, Platinum Mini Futures,
     Platinum Rolling-Spot Futures, Pocket Platinum 100 Futures,
     Palladium Futures)

    Day session  (JST): 08:45 – 15:45
    Night session (JST): 17:00 – 06:00 next day
    Modelled as: open=08:45, break_start=15:45, break_end=17:00, close=06:00+1.

    Night session is cancelled when the following calendar day is a holiday
    — not modelled (library limitation).

    Holidays: inherited from JPX.

    Source: https://www.jpx.co.jp/english/derivatives/rules/trading-hours/
    """

    aliases = ["OSE_PRECIOUS"]

    regular_market_times = {
        "market_open": ((None, time(8, 45)),),
        "market_close": ((None, time(6, 0), 1),),  # 06:00 JST next calendar day
        "break_start": ((None, time(15, 45)),),  # end of day session
        "break_end": ((None, time(17, 0)),),  # start of night session
    }

    @property
    def name(self):
        return "OSE_PRECIOUS"
