"""
Mainland China futures exchanges: SHFE, INE, DCE, CZCE, GFEX and CFFEX.

All six exchanges close on the same days as the Shanghai Stock Exchange (State Council holiday
notice + CSRC arrangement; weekend make-up workdays are not trading days), so the holiday rules and
ad hoc closures are shared with :class:`~pandas_market_calendars.calendars.sse.SSEExchangeCalendar`.
What the futures exchanges add is the night session, which no stock-exchange calendar can express:

* The common day session is 09:00-10:15, 10:30-11:30 and 13:30-15:00 Beijing time (CFFEX differs).
* Night sessions start at 21:00 and belong to the NEXT trading day: Friday evening is part of
  Monday's trading day, and the evening before a holiday closure has no night session, so the first
  trading day after a holiday is day-session only. The closing time of the night session depends on
  the product group (01:00, 02:30 or 23:00), hence one calendar per group.

Exchange-level calendars (``SHFE``, ``INE``, ``DCE``, ``CZCE``, ``GFEX``, ``CFFEX``, ``CFFEX_Bond``)
describe the day session that every product of the exchange trades. Product-group calendars
(``SHFE_BaseMetals`` ...) prepend the night session; product aliases such as ``SHFE_CU`` or ``DCE_I``
resolve to the group their product belongs to (as of 2026).

Sources: exchange trading-hours pages and holiday notices; product session times and the 2026 closure
dates were cross-checked against the open data published at https://futuresclock.com/en/data/ and
https://marketsopen.today/data (CC BY 4.0). Night-session history before the cut-over dates in
``holidays/cn_futures.py`` is modelled as day-session only.
"""

from abc import ABC, abstractmethod
from datetime import time
from typing import Any, List

import pandas as pd
from pandas.tseries.offsets import BDay, CustomBusinessDay
from zoneinfo import ZoneInfo

from pandas_market_calendars.calendars.sse import SSEExchangeCalendar
from pandas_market_calendars.holidays.cn import all_holidays
from pandas_market_calendars.holidays.cn_futures import (
    CZCE_NIGHT_FROM,
    DCE_NIGHT_FROM,
    INE_COPPER_NIGHT_FROM,
    INE_CRUDE_NIGHT_FROM,
    INE_INDUSTRIALS_NIGHT_FROM,
    NIGHT_SESSION_SUSPENDED_FROM,
    NIGHT_SESSION_SUSPENDED_TO,
    SHFE_BASE_METALS_NIGHT_FROM,
    SHFE_INDUSTRIALS_NIGHT_FROM,
    SHFE_PRECIOUS_METALS_NIGHT_FROM,
)
from pandas_market_calendars.market_calendar import MarketCalendar


# Common day session of the commodity exchanges (SHFE, INE, DCE, CZCE, GFEX).
COMMODITY_DAY_SESSION = {
    "market_open": ((None, time(9)),),
    "pause_start": ((None, time(10, 15)),),
    "pause_end": ((None, time(10, 30)),),
    "break_start": ((None, time(11, 30)),),
    "break_end": ((None, time(13, 30)),),
    "market_close": ((None, time(15)),),
}


def night_session_market_times(night_close: time, close_day_offset: int, night_from: str) -> dict:
    """
    Market times of a product group with a night session: the trading day opens at 21:00 on the previous
    evening, pauses at the night close and continues with the common day session from 09:00.

    :param night_close: local time at which the night session ends
    :param close_day_offset: day offset of ``night_close`` relative to the trading date (0 = same calendar
        day, e.g. 01:00; -1 = the previous evening, e.g. 23:00)
    :param night_from: first trading day that had a night session; earlier dates open at 09:00
    :return: ``regular_market_times`` dictionary
    """
    return {
        "market_open": ((None, time(9)), (night_from, time(21), -1)),
        "night_close": ((None, time(9)), (night_from, night_close, close_day_offset)),
        "day_open": ((None, time(9)),),
        **{k: v for k, v in COMMODITY_DAY_SESSION.items() if k != "market_open"},
    }


class ChinaFuturesBaseCalendar(MarketCalendar, ABC):
    """
    Common behaviour of the mainland China futures exchange calendars: Beijing time, Monday to Friday,
    and the same closures as the Shanghai Stock Exchange.
    """

    open_close_map = {
        **MarketCalendar.open_close_map,
        "pause_start": False,
        "pause_end": True,
        "night_close": False,
        "day_open": True,
    }

    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def tz(self) -> Any:
        return ZoneInfo("Asia/Shanghai")

    @property
    def regular_holidays(self) -> Any:
        # Same rule-based guesses for not-yet-announced years as the SSE calendar.
        return SSEExchangeCalendar.regular_holidays.fget(self)

    @property
    def adhoc_holidays(self) -> List[Any]:
        return all_holidays


class ChinaFuturesNightSessionCalendar(ChinaFuturesBaseCalendar, ABC):
    """
    A product group whose trading day starts with a night session at 21:00 Beijing time on the
    previous evening (``market_open``), pauses at ``night_close`` and resumes with the day session at
    ``day_open`` (09:00). Subclasses build ``regular_market_times`` with :func:`night_session_market_times`
    and set ``night_close_time`` / ``night_close_offset`` (relative to the trading date) and ``night_from``,
    the first trading day that had a night session.

    Special times implement the two calendar facts of night trading: Monday's trading day opens on
    Friday evening (``market_open`` and ``night_close`` shifted back by two more days), and the first
    trading day after a holiday closure opens at 09:00 because the evening before a closure has no
    night session (the 2020 suspension is treated the same way). On those day-session-only dates
    ``night_close`` is conformed to the 09:00 open.
    """

    night_from: str = "2013-07-05"
    night_close_time: time = time(1)
    night_close_offset: int = 0

    def _night_session_dates(self) -> Any:
        """
        Dates that need special night-session handling, from ``night_from`` to 2100.

        :return: tuple of (trading days with no night session, Mondays whose trading day starts on the
            preceding Friday evening)
        """
        start, end = pd.Timestamp(self.night_from), pd.Timestamp("2100-12-31")
        hol = pd.DatetimeIndex(self.holidays().holidays)
        hol = hol[(hol >= start - pd.Timedelta(days=14)) & (hol <= end) & (hol.weekday < 5)]
        after_holiday = (hol + BDay(1)).unique()
        after_holiday = after_holiday[~after_holiday.isin(hol)]
        suspended = pd.date_range(
            NIGHT_SESSION_SUSPENDED_FROM,
            NIGHT_SESSION_SUSPENDED_TO,
            freq=self.holidays(),
        )
        day_only = after_holiday.union(suspended)
        day_only = day_only[day_only >= start]
        mondays = pd.date_range(start, end, freq=CustomBusinessDay(weekmask="Mon"))
        mondays = mondays[~mondays.isin(day_only)]
        return day_only, mondays

    @property
    def special_opens_adhoc(self) -> List[Any]:
        day_only, mondays = self._night_session_dates()
        return [(time(9), day_only), ((time(21), -3), mondays)]

    @property
    def special_night_close_adhoc(self) -> List[Any]:
        _, mondays = self._night_session_dates()
        return [((self.night_close_time, self.night_close_offset - 2), mondays)]


# --- Exchange-level day-session calendars ----------------------------------------------------------


class SHFEExchangeCalendar(ChinaFuturesBaseCalendar):
    """
    Shanghai Futures Exchange, day session: 09:00-10:15, 10:30-11:30, 13:30-15:00 Beijing time.
    Night sessions are product-specific; see SHFE_BaseMetals, SHFE_PreciousMetals, SHFE_Industrials.
    https://www.shfe.com.cn/
    """

    aliases = ["SHFE", "SHFE_Day"]
    regular_market_times = COMMODITY_DAY_SESSION

    @property
    def name(self) -> str:
        return "SHFE"

    @property
    def full_name(self) -> str:
        return "Shanghai Futures Exchange"


class INEExchangeCalendar(ChinaFuturesBaseCalendar):
    """
    Shanghai International Energy Exchange (INE, an SHFE subsidiary), day session. Night sessions:
    see INE_Crude, INE_Copper, INE_Industrials. Container freight (EC) trades the day session only.
    https://www.ine.cn/
    """

    aliases = ["INE", "INE_Day", "INE_EC"]
    regular_market_times = COMMODITY_DAY_SESSION

    @property
    def name(self) -> str:
        return "INE"

    @property
    def full_name(self) -> str:
        return "Shanghai International Energy Exchange"


class DCEExchangeCalendar(ChinaFuturesBaseCalendar):
    """
    Dalian Commodity Exchange, day session. Night session (21:00-23:00): see DCE_Night.
    Live hog (LH) and eggs trade the day session only.
    http://www.dce.com.cn/
    """

    aliases = ["DCE", "DCE_Day", "DCE_LH"]
    regular_market_times = COMMODITY_DAY_SESSION

    @property
    def name(self) -> str:
        return "DCE"

    @property
    def full_name(self) -> str:
        return "Dalian Commodity Exchange"


class CZCEExchangeCalendar(ChinaFuturesBaseCalendar):
    """
    Zhengzhou Commodity Exchange, day session. Night session (21:00-23:00): see CZCE_Night.
    Apples, ferrosilicon, silicomanganese and urea trade the day session only.
    http://www.czce.com.cn/
    """

    aliases = ["CZCE", "ZCE", "CZCE_Day", "CZCE_AP", "CZCE_SF", "CZCE_SM", "CZCE_UR"]
    regular_market_times = COMMODITY_DAY_SESSION

    @property
    def name(self) -> str:
        return "CZCE"

    @property
    def full_name(self) -> str:
        return "Zhengzhou Commodity Exchange"


class GFEXExchangeCalendar(ChinaFuturesBaseCalendar):
    """
    Guangzhou Futures Exchange. Day session only (industrial silicon, lithium carbonate, polysilicon,
    platinum): 09:00-10:15, 10:30-11:30, 13:30-15:00 Beijing time.
    http://www.gfex.com.cn/
    """

    aliases = ["GFEX", "GFEX_SI", "GFEX_LC", "GFEX_PS", "GFEX_PT"]
    regular_market_times = COMMODITY_DAY_SESSION

    @property
    def name(self) -> str:
        return "GFEX"

    @property
    def full_name(self) -> str:
        return "Guangzhou Futures Exchange"


class CFFEXExchangeCalendar(ChinaFuturesBaseCalendar):
    """
    China Financial Futures Exchange, equity index futures and options (IF, IH, IC, IM):
    09:30-11:30, 13:00-15:00 Beijing time, no night session.
    http://www.cffex.com.cn/
    """

    aliases = ["CFFEX", "CFFEX_Equity", "CFFEX_IF", "CFFEX_IH", "CFFEX_IC", "CFFEX_IM"]
    regular_market_times = {
        "market_open": ((None, time(9, 30)),),
        "break_start": ((None, time(11, 30)),),
        "break_end": ((None, time(13)),),
        "market_close": ((None, time(15)),),
    }

    @property
    def name(self) -> str:
        return "CFFEX"

    @property
    def full_name(self) -> str:
        return "China Financial Futures Exchange"


class CFFEXBondExchangeCalendar(CFFEXExchangeCalendar):
    """
    China Financial Futures Exchange, treasury bond futures (TS, TF, T, TL):
    09:30-11:30, 13:00-15:15 Beijing time, no night session.
    """

    aliases = ["CFFEX_Bond", "CFFEX_TS", "CFFEX_TF", "CFFEX_T", "CFFEX_TL"]
    regular_market_times = {
        **CFFEXExchangeCalendar.regular_market_times,
        "market_close": ((None, time(15, 15)),),
    }

    @property
    def name(self) -> str:
        return "CFFEX_Bond"


# --- Product-group calendars with night sessions ---------------------------------------------------


class SHFEBaseMetalsCalendar(ChinaFuturesNightSessionCalendar):
    """SHFE copper, aluminium, zinc, lead, nickel, tin, stainless steel, alumina: night 21:00-01:00."""

    aliases = [
        "SHFE_BaseMetals",
        "SHFE_CU",
        "SHFE_AL",
        "SHFE_ZN",
        "SHFE_PB",
        "SHFE_NI",
        "SHFE_SN",
        "SHFE_SS",
        "SHFE_AO",
    ]
    regular_market_times = night_session_market_times(time(1), 0, SHFE_BASE_METALS_NIGHT_FROM)
    night_close_time = time(1)
    night_close_offset = 0
    night_from = SHFE_BASE_METALS_NIGHT_FROM

    @property
    def name(self) -> str:
        return "SHFE_BaseMetals"


class SHFEPreciousMetalsCalendar(ChinaFuturesNightSessionCalendar):
    """SHFE gold and silver: night 21:00-02:30."""

    aliases = ["SHFE_PreciousMetals", "SHFE_AU", "SHFE_AG"]
    regular_market_times = night_session_market_times(time(2, 30), 0, SHFE_PRECIOUS_METALS_NIGHT_FROM)
    night_close_time = time(2, 30)
    night_close_offset = 0
    night_from = SHFE_PRECIOUS_METALS_NIGHT_FROM

    @property
    def name(self) -> str:
        return "SHFE_PreciousMetals"


class SHFEIndustrialsCalendar(ChinaFuturesNightSessionCalendar):
    """SHFE rebar, hot-rolled coil, natural rubber, bitumen, fuel oil, pulp: night 21:00-23:00."""

    aliases = [
        "SHFE_Industrials",
        "SHFE_RB",
        "SHFE_HC",
        "SHFE_RU",
        "SHFE_BU",
        "SHFE_FU",
        "SHFE_SP",
    ]
    regular_market_times = night_session_market_times(time(23), -1, SHFE_INDUSTRIALS_NIGHT_FROM)
    night_close_time = time(23)
    night_close_offset = -1
    night_from = SHFE_INDUSTRIALS_NIGHT_FROM

    @property
    def name(self) -> str:
        return "SHFE_Industrials"


class INECrudeCalendar(ChinaFuturesNightSessionCalendar):
    """INE crude oil (SC): night 21:00-02:30."""

    aliases = ["INE_Crude", "INE_SC"]
    regular_market_times = night_session_market_times(time(2, 30), 0, INE_CRUDE_NIGHT_FROM)
    night_close_time = time(2, 30)
    night_close_offset = 0
    night_from = INE_CRUDE_NIGHT_FROM

    @property
    def name(self) -> str:
        return "INE_Crude"


class INECopperCalendar(ChinaFuturesNightSessionCalendar):
    """INE international copper (BC): night 21:00-01:00."""

    aliases = ["INE_Copper", "INE_BC"]
    regular_market_times = night_session_market_times(time(1), 0, INE_COPPER_NIGHT_FROM)
    night_close_time = time(1)
    night_close_offset = 0
    night_from = INE_COPPER_NIGHT_FROM

    @property
    def name(self) -> str:
        return "INE_Copper"


class INEIndustrialsCalendar(ChinaFuturesNightSessionCalendar):
    """INE low-sulphur fuel oil (LU) and TSR 20 rubber (NR): night 21:00-23:00."""

    aliases = ["INE_Industrials", "INE_LU", "INE_NR"]
    regular_market_times = night_session_market_times(time(23), -1, INE_INDUSTRIALS_NIGHT_FROM)
    night_close_time = time(23)
    night_close_offset = -1
    night_from = INE_INDUSTRIALS_NIGHT_FROM

    @property
    def name(self) -> str:
        return "INE_Industrials"


class DCENightCalendar(ChinaFuturesNightSessionCalendar):
    """DCE products with a night session (soybeans, meal, oils, corn, iron ore, coke, coking coal, chemicals, LPG): 21:00-23:00."""

    aliases = [
        "DCE_Night",
        "DCE_A",
        "DCE_M",
        "DCE_Y",
        "DCE_P",
        "DCE_C",
        "DCE_I",
        "DCE_J",
        "DCE_JM",
        "DCE_L",
        "DCE_V",
        "DCE_PP",
        "DCE_EG",
        "DCE_EB",
        "DCE_PG",
    ]
    regular_market_times = night_session_market_times(time(23), -1, DCE_NIGHT_FROM)
    night_close_time = time(23)
    night_close_offset = -1
    night_from = DCE_NIGHT_FROM

    @property
    def name(self) -> str:
        return "DCE_Night"


class CZCENightCalendar(ChinaFuturesNightSessionCalendar):
    """CZCE products with a night session (cotton, sugar, PTA, methanol, rapeseed oil/meal, glass, soda ash, PX, PF, caustic soda): 21:00-23:00."""

    aliases = [
        "CZCE_Night",
        "CZCE_CF",
        "CZCE_SR",
        "CZCE_TA",
        "CZCE_MA",
        "CZCE_OI",
        "CZCE_RM",
        "CZCE_FG",
        "CZCE_SA",
        "CZCE_PF",
        "CZCE_PX",
        "CZCE_SH",
    ]
    regular_market_times = night_session_market_times(time(23), -1, CZCE_NIGHT_FROM)
    night_close_time = time(23)
    night_close_offset = -1
    night_from = CZCE_NIGHT_FROM

    @property
    def name(self) -> str:
        return "CZCE_Night"
