from .market_calendar import MarketCalendar
from .exchange_calendars.asx import ASXExchangeCalendar
from .exchange_calendars.bmf import BMFExchangeCalendar
from .exchange_calendars.cme import \
    CMEEquityExchangeCalendar, \
    CMEBondExchangeCalendar
from .exchange_calendars.cme_globex_crypto import CMEGlobexCryptoExchangeCalendar
from .exchange_calendars.cme_globex_fx import CMEGlobexFXExchangeCalendar
from .exchange_calendars.cme_globex_fixed_income import CMEGlobexFixedIncomeCalendar
from .exchange_calendars.eurex import EUREXExchangeCalendar
from .exchange_calendars.hkex import HKEXExchangeCalendar
from .exchange_calendars.jpx import JPXExchangeCalendar
from .exchange_calendars.ose import OSEExchangeCalendar
from .exchange_calendars.six import SIXExchangeCalendar
from .exchange_calendars.mirror import *


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
