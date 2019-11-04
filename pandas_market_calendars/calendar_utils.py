"""
Utilities to use with market_calendars
"""
################## >>> Deprecated (remove in future releases)
import warnings
from collections.abc import MutableMapping

import pandas as pd

from . import calendar_registry


class DeprecatedRegistry(MutableMapping):

    def __init__(self):
        self._dict = calendar_registry.MarketCalendar._regmeta_class_registry

    def _warn(self):
        warnings.warn(
            """
            This dictionary will be removed from calendar_utils in future releases. 
            Market Calendar's are registered automatically and there is no longer any 
            need to access the registry directly."""
        )

    def __getitem__(self, key):
        self._warn()
        return self._dict[key]

    def __setitem__(self, key, value):
        self._warn()
        self._dict[key] = value

    def __delitem__(self, key):
        self._warn()
        del self._dict[key]

    def __iter__(self):
        self._warn()
        return iter(self._dict)

    def __len__(self):
        self._warn()
        return len(self._dict)

_calendars = _aliases = DeprecatedRegistry()

def get_calendar(*args,**kwargs):
    warnings.warn(
            """
            get_calendar has moved from calendar_utils to market_calendar. 
            It will be removed from calendar_utils in future releases.""",
            DeprecationWarning
        )
    calendar_registry.get_calendar(*args,**kwargs)

################## <<< Deprecated (remove in future releases)

def merge_schedules(schedules, how='outer'):
    """
    Given a list of schedules will return a merged schedule. The merge method (how) will either return the superset
    of any datetime when any schedule is open (outer) or only the datetime where all markets are open (inner)

    :param schedules: list of schedules
    :param how: outer or inner
    :return: schedule DataFrame
    """

    result = schedules[0]
    for schedule in schedules[1:]:
        result = result.merge(schedule, how=how, right_index=True, left_index=True)
        if how == 'outer':
            result['market_open'] = result.apply(lambda x: min(x.market_open_x, x.market_open_y), axis=1)
            result['market_close'] = result.apply(lambda x: max(x.market_close_x, x.market_close_y), axis=1)
        elif how == 'inner':
            result['market_open'] = result.apply(lambda x: max(x.market_open_x, x.market_open_y), axis=1)
            result['market_close'] = result.apply(lambda x: min(x.market_close_x, x.market_close_y), axis=1)
        else:
            raise ValueError('how argument must be "inner" or "outer"')
        result = result[['market_open', 'market_close']]
    return result


def convert_freq(index, frequency):
    """
    Converts a DateTimeIndex to a new lower frequency

    :param index: DateTimeIndex
    :param frequency: frequency string
    :return: DateTimeIndex
    """
    return pd.DataFrame(index=index).asfreq(frequency).index


def date_range(schedule, frequency, closed='right', force_close=True, **kwargs):
    """
    Given a schedule will return a DatetimeIndex will all of the valid datetime at the frequency given.
    The schedule values are assumed to be in UTC.

    :param schedule: schedule DataFrame
    :param frequency: frequency in standard string
    :param closed: same meaning as pandas date_range. 'right' will exclude the first value and should be used when the
      results should only include the close for each bar.
    :param force_close: if True then the close of the day will be included even if it does not fall on an even
      frequency. If False then the market close for the day may not be included in the results
    :param kwargs: arguments that will be passed to the pandas date_time
    :return: DatetimeIndex
    """

    if pd.Timedelta(frequency) > pd.Timedelta('1D'):
        raise ValueError('Frequency must be 1D or higher frequency.')
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
