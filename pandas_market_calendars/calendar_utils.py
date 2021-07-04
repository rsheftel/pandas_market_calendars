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
    Given a schedule will return a DatetimeIndex with all of the valid datetime at the frequency given.
    The schedule values are assumed to be in UTC.

    :param schedule: schedule DataFrame
    :param frequency: frequency in standard string
    :param closed: same meaning as pandas date_range. 'right' will exclude the first value and should be used when the
      results should only include the close for each bar.
    :param force_close: if True then the close of the day will be included even if it does not fall on an even
      frequency. If False then the market close for the day may not be included in the results
    :param kwargs: unused
    :return: DatetimeIndex
    """

    frequency, daily = pd.Timedelta(frequency), pd.Timedelta("1D")
    if frequency > daily: raise ValueError('Frequency must be 1D or higher frequency.')
    elif schedule.empty: return pd.DatetimeIndex([], tz= "UTC")

    # daily can be handled more efficiently, seperately
    if frequency == daily:
        if closed == "right":
            if force_close is False: return pd.DatetimeIndex([], tz= "UTC")
            index = pd.DatetimeIndex(schedule.market_close, tz= "UTC")
        else:
            if force_close:
                index = pd.DatetimeIndex(pd.concat(
                    [schedule.market_open, schedule.market_close]).sort_values(), tz= "UTC")
            else:
                index = pd.DatetimeIndex(schedule.market_open, tz="UTC")
        index.name = None
        return index

    # if not daily, calculate n bars required for each day,
    # then create series with market_open and market_closes repeated n times
    num_bars = (schedule.market_close - schedule.market_open) / frequency
    _remains = num_bars % 1    # round up, np.ceil-style
    num_bars = num_bars.where(_remains == 0, num_bars + 1 - _remains).astype("int")
    opens = schedule.market_open.repeat(num_bars)
    closes = schedule.market_close.repeat(num_bars)

    # ---> calculate the desired timeseries:
    index_to_be = opens.groupby(opens.index).cumcount() * frequency + opens

    # handle the closed/force_close parameters if needed
    if closed != "left":
        index_to_be += frequency # shift the timeseries by frequency
        index_to_be = index_to_be[index_to_be.le(closes)]  # make sure market_close is the max value
        if closed is None: # add the market_open
            index_to_be = pd.concat([index_to_be, schedule.market_open]).sort_values()

    if force_close: # add the market close
        print("adding")
        index_to_be = pd.concat([index_to_be, schedule.market_close]).sort_values()
        index_to_be = index_to_be.drop_duplicates() # since it may already be in there

    index_to_be = index_to_be.reset_index(drop= True)
    if "break_start" in schedule.columns:

        # new num_bars after closed= None/force_close= True were applied
        num_bars = index_to_be.groupby(index_to_be.dt.date).size()
        start = schedule.break_start.repeat(num_bars).reset_index(drop= True)
        end = schedule.break_end.repeat(num_bars).reset_index(drop= True)

        if closed == "right":
            index_to_be = index_to_be[index_to_be.le(start) | index_to_be.gt(end)]
        elif closed == "left":
            index_to_be = index_to_be[index_to_be.lt(start) | index_to_be.ge(end)]
        else:
            index_to_be = index_to_be[index_to_be.le(start) | index_to_be.ge(end)]

    return pd.DatetimeIndex(index_to_be, tz= "UTC")
