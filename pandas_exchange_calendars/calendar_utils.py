from pandas_exchange_calendars.exchange_calendar_cfe import CFEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_ice import ICEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_nyse import NYSEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_cme import CMEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_bmf import BMFExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_lse import LSEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_tsx import TSXExchangeCalendar
from .us_futures_calendar import QuantopianUSFuturesCalendar

_calendars = {
    'NYSE': NYSEExchangeCalendar,
    'CME': CMEExchangeCalendar,
    'ICE': ICEExchangeCalendar,
    'CFE': CFEExchangeCalendar,
    'BMF': BMFExchangeCalendar,
    'LSE': LSEExchangeCalendar,
    'TSX': TSXExchangeCalendar,
    'us_futures': QuantopianUSFuturesCalendar,
}
_aliases = {
    'NASDAQ': 'NYSE',
    'BATS': 'NYSE',
    'CBOT': 'CME',
    'COMEX': 'CME',
    'NYMEX': 'CME',
    'ICEUS': 'ICE',
    'NYFE': 'ICE',
}


def get_calendar(name):
    """
    Retrieves an instance of an ExchangeCalendar whose name is given.

    Parameters
    ----------
    name : str
        The name of the ExchangeCalendar to be retrieved.

    Returns
    -------
    ExchangeCalendar
        The desired calendar.
    """
    canonical_name = _aliases.get(name, name)
    return _calendars[canonical_name]()
