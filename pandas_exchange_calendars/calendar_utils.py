
import pandas as pd
from pandas_exchange_calendars.exchange_calendar_cfe import CFEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_ice import ICEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_nyse import NYSEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_cme import CMEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_bmf import BMFExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_lse import LSEExchangeCalendar
from pandas_exchange_calendars.exchange_calendar_tsx import TSXExchangeCalendar

_calendars = {
    'NYSE': NYSEExchangeCalendar,
    'CME': CMEExchangeCalendar,
    'ICE': ICEExchangeCalendar,
    'CFE': CFEExchangeCalendar,
    'BMF': BMFExchangeCalendar,
    'LSE': LSEExchangeCalendar,
    'TSX': TSXExchangeCalendar
}

_aliases = {
    'stock': 'NYSE',
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


def merge_schedules(schedules, how='outer'):
    pass


def date_range(schedule, frequency, closed='right', force_close=True, **kwargs):
    """
    The schedule values are assumed to be in UTC

    :param schedule:
    :param frequency:
    :param closed:
    :param force_close:
    :param kwargs:
    :return:
    """
    kwargs['closed'] = closed
    ranges = list()
    for row in schedule.itertuples():
        dates = pd.date_range(row.market_open, row.market_close, freq=frequency, tz='UTC', **kwargs)
        if force_close:
            if row.market_close not in dates:
                dates = dates.insert(len(dates), row.market_close)
        ranges.append(dates)

    index = pd.DatetimeIndex([], tz='UTC')
    return index.union_many(ranges)
