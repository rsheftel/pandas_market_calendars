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

def _calc_time_series(schedule, frequency, closed, force_close):
    """
    Function used by date_range to calculate the trading index.
    """
    _open, _close = schedule

    # Calculate number of bars for each day, drop any days with no required rows
    num_bars = (schedule[_close] - schedule[_open]) / frequency
    above_zero = num_bars.gt(0)
    if not above_zero.all():
        schedule = schedule[above_zero]; num_bars = num_bars[above_zero]

    remains = num_bars % 1    # round up, np.ceil-style
    num_bars = num_bars.where(remains == 0, num_bars + 1 - remains).round()

    # ---> calculate the desired timeseries:
    if closed == "left":
        opens = schedule[_open].repeat(num_bars)   # keep as is
        time_series = (opens.groupby(opens.index).cumcount()) * frequency + opens
    elif closed == "right":
        opens = schedule[_open].repeat(num_bars)   # dont add row but shift up
        time_series = (opens.groupby(opens.index).cumcount()+ 1) * frequency + opens
    elif closed in (None, "both"):
        num_bars += 1
        opens = schedule[_open].repeat(num_bars)   # add row but dont shift up
        time_series = (opens.groupby(opens.index).cumcount()) * frequency + opens
    else: # closed == "neither"
        num_bars -= 1
        opens = schedule[_open].repeat(num_bars)   # remove row and shift up
        time_series = (opens.groupby(opens.index).cumcount()+ 1) * frequency + opens

    if force_close:
        time_series = time_series[time_series.lt(schedule[_close].repeat(num_bars))]
        time_series = pd.concat([time_series, schedule[_close]]).sort_values()

    return time_series

def date_range(schedule, frequency, closed='right', force_close=True, **kwargs):
    """
    NEGATIVES: ??

        Raise a warning
        raise error  <<<
        handle the same way as before

        --> create a function that allows to shift the closing times?

    closed =
        * "left" - include left indice of first interval/bar, do not include right indice of last interval/bar.
        * "right" - do not include left indice of first interval, include right indice of last interval.
        * None/"both" - closed = "left" and force = True

    force_close =
        * True      will make sure close is last value of day
        * False     will make sure that nothing larger than close exists
        * None      will not force anything

    sample
        freq 1h
        open 9
        close 11.30
        num_bars = 3

    permutations

        9 10 11        left False/ left None/ both False
        9 10 11 11.30  left True/ both True
        10 11          right False
        10 11 11.30    right True
        10 11 12       right None
        9 10 11 12     both None

        left True
        left False
        left None
        right True
        right False
        right None
        both True
        both False
        both None



        9 10 11        left None
        9 10 11 11.30  left True/  both True
        10 11          neither False
        10 11 11.30     neither True/  right True
        10 11 12         right False
        9 10 11 12     both False

        left True
        left False
        right True
        right False
        both True
        both False
        neither True
        neither False

    """
    frequency, daily = pd.Timedelta(frequency), pd.Timedelta("1D")
    if frequency > daily:
        raise ValueError('Frequency must be 1D or higher frequency.')

    elif schedule.market_close.le(schedule.market_open).any():
        raise ValueError("Schedule contains rows where market_close <= market_open,"
                         " please correct the schedule")

    isdaily = frequency == daily
    if isdaily and not force_close:
        if closed in ("neither", "right"): return pd.DatetimeIndex([], tz= "UTC")
        if closed in (None, "both", "left"): time_series = schedule.market_open

    elif "break_start" in schedule.columns and not isdaily:
        time_series = pd.concat([
                _calc_time_series(schedule[["market_open", "break_start"]], frequency, closed, force_close),
                _calc_time_series(schedule[["break_end", "market_close"]], frequency, closed, force_close)
        ]).sort_values()
        # should probably add a check for overlapping indices that don't make any sense before concatenating
    else:
        time_series = _calc_time_series(schedule, frequency, closed, force_close)

    time_series.name = None
    return pd.DatetimeIndex(time_series, tz= "UTC")

def old_date_range(schedule, frequency, closed='right', force_close=True, **kwargs):
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

    Two Caveats (that also apply to the old version):

        * If the difference between market close and open is smaller than frequency
        and closed= "right" and force_close = False:
        ----> the whole day will just disappear

        * If the market close is before the market open, it will only return something
        if force_close = True, and then it will *only* return the closes of each day,
        regardless of the frequency
    """
    frequency = pd.Timedelta(frequency)
    if frequency > pd.Timedelta("1D"): raise ValueError('Frequency must be 1D or higher frequency.')

    # some markets/tests contain rows where the close is before the open,
    # which the original function drops completely *unless* force_close adds the close anyway
    difference = schedule.market_close - schedule.market_open
    negative = difference.lt(pd.Timedelta(0))
    if negative.any():
        any_neg = True
        negatives = schedule[negative].market_close if force_close else [] # keep closes to concat later
        schedule, difference = schedule[~negative], difference[~negative]
    else: any_neg= False

    # Calculate number of bars for each day
    num_bars = difference / frequency
    remains = num_bars % 1    # round up, np.ceil-style
    num_bars = num_bars.where(remains == 0, num_bars + 1 - remains).round()

    # ---> calculate the desired timeseries:
    if closed == "right":
        opens = schedule.market_open.repeat(num_bars)   # dont add row but shift up
        index_to_be = (opens.groupby(opens.index).cumcount()+ 1) * frequency + opens
    elif closed is None or force_close:
        num_bars += 1
        opens = schedule.market_open.repeat(num_bars)   # add row but dont shift up
        index_to_be = (opens.groupby(opens.index).cumcount()) * frequency + opens
    else:
        opens = schedule.market_open.repeat(num_bars)   # keep as is
        index_to_be = (opens.groupby(opens.index).cumcount()) * frequency + opens

    # add close or drop everything larger than close, depending on force_close/negatives
    closes = schedule.market_close.repeat(num_bars)
    if force_close:
        index_to_be = index_to_be.where(index_to_be.le(closes), closes)
        if any_neg:
            index_to_be = pd.concat([index_to_be, negatives]).sort_values()
    else: index_to_be = index_to_be[index_to_be.le(closes)]

    # handle potential breaks
    if "break_start" in schedule.columns:
        num_bars = index_to_be.groupby(index_to_be.index).size() # may have changed
        start = schedule.break_start.loc[num_bars.index].repeat(num_bars) # need to be aligned
        end = schedule.break_end.loc[num_bars.index].repeat(num_bars)
        if closed == "right":
            index_to_be = index_to_be[index_to_be.le(start) | index_to_be.gt(end)]
        elif closed == "left":
            index_to_be = index_to_be[index_to_be.lt(start) | index_to_be.ge(end)]
        else:
            index_to_be = index_to_be[index_to_be.le(start) | index_to_be.ge(end)]

    index_to_be.name = None
    return pd.DatetimeIndex(index_to_be.drop_duplicates().sort_values(), tz= "UTC")
