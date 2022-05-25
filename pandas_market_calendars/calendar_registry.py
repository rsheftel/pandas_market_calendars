from .market_calendar import MarketCalendar
from .exchange_calendar_asx import ASXExchangeCalendar
from .exchange_calendar_bmf import BMFExchangeCalendar
from .exchange_calendar_cboe import CFEExchangeCalendar
from .exchange_calendar_cme import \
    CMEEquityExchangeCalendar, \
    CMEBondExchangeCalendar
from .exchange_calendar_cme_globex_base import CMEGlobexBaseExchangeCalendar
from .exchange_calendar_cme_globex_agriculture import CMEGlobexAgricultureExchangeCalendar
from .exchange_calendar_cme_globex_fx import CMEGlobexFXExchangeCalendar
from .exchange_calendar_cme_globex_energy_and_metals import CMEGlobexEnergyAndMetalsExchangeCalendar
from .exchange_calendar_cme_globex_equities import CMEGlobexEquitiesExchangeCalendar
from .exchange_calendar_cme_globex_fixed_income import CMEGlobexFixedIncomeCalendar
from .exchange_calendar_eurex import EUREXExchangeCalendar
from .exchange_calendar_hkex import HKEXExchangeCalendar
from .exchange_calendar_ice import ICEExchangeCalendar
from .exchange_calendar_iex import IEXExchangeCalendar
from .exchange_calendar_jpx import JPXExchangeCalendar
from .exchange_calendar_lse import LSEExchangeCalendar
from .exchange_calendar_nyse import NYSEExchangeCalendar
from .exchange_calendar_ose import OSEExchangeCalendar
from .exchange_calendar_sifma import SIFMAUSExchangeCalendar, SIFMAUKExchangeCalendar, SIFMAJPExchangeCalendar
from .exchange_calendar_six import SIXExchangeCalendar
from .exchange_calendar_sse import SSEExchangeCalendar
from .exchange_calendar_tsx import TSXExchangeCalendar
from .exchange_calendar_bse import BSEExchangeCalendar
from .exchange_calendar_tase import TASEExchangeCalendar
from .exchange_calendars_mirror import *


def get_calendar(name, open_time=None, close_time=None):
    """
    Retrieves an instance of an MarketCalendar whose name is given.

    :param name: The name of the MarketCalendar to be retrieved.
    :param open_time: Market open time override as datetime.time object. If None then default is used.
    :param close_time: Market close time override as datetime.time object. If None then default is used.
    :return: MarketCalendar of the desired calendar.
    """
    return MarketCalendar.factory(name, open_time=open_time, close_time=close_time)


def get_calendar_names():
    """All Market Calendar names and aliases that can be used in "factory"
    :return: list(str)
    """
    return MarketCalendar.calendar_names()
