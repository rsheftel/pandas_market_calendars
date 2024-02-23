from .market_calendar import MarketCalendar
from .calendars.asx import ASXExchangeCalendar
from .calendars.bmf import BMFExchangeCalendar
from .calendars.bse import BSEExchangeCalendar
from .calendars.cboe import CFEExchangeCalendar
from .calendars.cme import CMEEquityExchangeCalendar, CMEBondExchangeCalendar
from .calendars.cme_globex_base import CMEGlobexBaseExchangeCalendar
from .calendars.cme_globex_agriculture import (
    CMEGlobexAgricultureExchangeCalendar,
    CMEGlobexLivestockExchangeCalendar,
    CMEGlobexGrainsAndOilseedsExchangeCalendar,
)
from .calendars.cme_globex_crypto import CMEGlobexCryptoExchangeCalendar
from .calendars.cme_globex_energy_and_metals import (
    CMEGlobexEnergyAndMetalsExchangeCalendar,
)
from .calendars.cme_globex_equities import CMEGlobexEquitiesExchangeCalendar
from .calendars.cme_globex_fx import CMEGlobexFXExchangeCalendar
from .calendars.cme_globex_fixed_income import CMEGlobexFixedIncomeCalendar
from .calendars.eurex import EUREXExchangeCalendar
from .calendars.eurex_fixed_income import EUREXFixedIncomeCalendar
from .calendars.hkex import HKEXExchangeCalendar
from .calendars.ice import ICEExchangeCalendar
from .calendars.iex import IEXExchangeCalendar
from .calendars.jpx import JPXExchangeCalendar
from .calendars.lse import LSEExchangeCalendar
from .calendars.nyse import NYSEExchangeCalendar
from .calendars.ose import OSEExchangeCalendar
from .calendars.sifma import (
    SIFMAUSExchangeCalendar,
    SIFMAUKExchangeCalendar,
    SIFMAJPExchangeCalendar,
)
from .calendars.six import SIXExchangeCalendar
from .calendars.sse import SSEExchangeCalendar
from .calendars.tase import TASEExchangeCalendar
from .calendars.tsx import TSXExchangeCalendar
from .calendars.mirror import *


def get_calendar(name, open_time=None, close_time=None) -> MarketCalendar:
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
