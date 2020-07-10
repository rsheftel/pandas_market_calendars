"""
Utilities to use with market_calendars
"""
import itertools
import warnings

import pandas as pd


def merge_schedules(schedules, how='outer'):
    """
    Given a list of schedules will return a merged schedule. The merge method (how) will either return the superset
    of any datetime when any schedule is open (outer) or only the datetime where all markets are open (inner)
     *NOTE* This does not work for schedules with breaks, the break information will be lost.

    :param schedules: list of schedules
    :param how: outer or inner
    :return: schedule DataFrame
    """

    all_cols = [x.columns for x in schedules]
    all_cols = list(itertools.chain(*all_cols))
    if ('break_start' in all_cols) or ('break_end' in all_cols):
        warnings.warn('Merge schedules will drop the break_start and break_end from result.')

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
    breaks = 'break_start' in schedule.columns
    for row in schedule.itertuples():
        dates = pd.date_range(row.market_open, row.market_close, freq=frequency, tz='UTC', **kwargs)
        if force_close:
            if row.market_close not in dates:
                dates = dates.insert(len(dates), row.market_close)
        if breaks:
            if closed == 'right':
                dates = dates[(dates <= row.break_start) | (row.break_end < dates)]
            elif closed == 'left':
                dates = dates[(dates < row.break_start) | (row.break_end <= dates)]
            else:
                dates = dates[(dates <= row.break_start) | (row.break_end <= dates)]

        ranges.append(dates)

    index = pd.DatetimeIndex([], tz='UTC')
    return index.union_many(ranges)
