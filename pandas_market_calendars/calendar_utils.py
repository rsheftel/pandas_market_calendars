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

class _date_range:
    """
    This is a callable class that should be used by calling the already initiated instance: `date_range`

    Signature:
    .__call__(self, schedule, frequency, closed='right', force_close=True, **kwargs)

    :param schedule: schedule of a calendar, which may or may not include break_start and break_end columns
    :param frequency: frequency string that is used by pd.Timedelta to calculate the timestamps
        this must be "1D" or higher
    :param closed: the way the intervals are labeled
        'right': use the end of the interval
        'left': use the start of the interval
        None: (or 'both') use the end of the interval but include the start of the first interval
    :param force_close: how the last value of a trading session is handled
        True: guarantee that the close of the trading session is the last value
        False: guarantee that there is no value greater than the close of the trading session
        None: leave the last value as it is calculated based on the closed parameter
    :param kwargs: unused. Solely for compatibility.

    Caveats:
    * A trading session is either from market_open to market_close, or, if break_start and break_end are provided,
        from market_open to break_start and from break_end to market_close.
      The calculation based on frequency, closed and force_close is made for each trading session, this means
      that break_start is considered the close of the first session of a trading day and break_end is considered
      the open of the second session of the trading day

    * If the difference between start and end of a trading session is smaller than frequency
        and closed= "right" and force_close = False, the whole session will just disappear




    """

    before, after = ["market_open", "break_start"], ["break_end", "market_close"]

    def __init__(self, schedule = None, frequency= None, closed='right', force_close=True):
        if not closed in ("left", "right", "both", None):
            raise ValueError("closed must be 'left', 'right', 'both' or None.")
        elif not force_close in (True, False, None):
            raise ValueError("force_close must be True, False or None.")

        self.closed = closed
        self.force_close = force_close
        self._overlap_danger = force_close is None and closed != "left"
        self.has_breaks = False
        if frequency is None: self.frequency = None
        else:
            self.frequency = pd.Timedelta(frequency)
            if self.frequency > pd.Timedelta("1D"):
                raise ValueError('Frequency must be 1D or higher frequency.')

            elif schedule.market_close.le(schedule.market_open).any():
                raise ValueError("Schedule contains rows where market_close <= market_open,"
                                 " please correct the schedule")

            if "break_start" in schedule:
                if not all([
                    schedule.market_open.le(schedule.break_start).all(),
                    schedule.break_start.le(schedule.break_end).all(),
                    schedule.break_end.le(schedule.market_close).all()]):
                    raise ValueError("Not all rows match the condition: "
                                     "market_open <= break_start <= break_end <= market_close, "
                                     "please correct the schedule")
                # ---> Dec 23rd 2020 in XHKG break_start > market_close and break_end < break_start ...
                self.has_breaks = True


    def _check_overlap(self, schedule, limit):
        """checks if calculated end times would overlap with the next start times.
        :param schedule: pd.DataFrame with start times in first column and end times in second column
        :param limit: next start time
        """
        num_bars = self._calc_num_bars(schedule)
        end_times = schedule.iloc[:, 0] + num_bars * self.frequency
        if end_times.gt(limit).any():
            raise ValueError(f"The chosen frequency will lead to overlaps in the calculated index. "
                             f"Either choose a higher frequency or avoid setting force_close to None "
                             f"when setting closed to 'right', 'both' or None.")

    def _calc_num_bars(self, schedule):
        """
        :param schedule: pd.DataFrame with start times in first column and end times in second column
        :return: pd.Series of integers"""
        num_bars = (schedule.iloc[:, 1] - schedule.iloc[:, 0]) / self.frequency
        remains = num_bars % 1    # round up, np.ceil-style
        return num_bars.where(remains == 0, num_bars + 1 - remains).round()

    def _calc_time_series(self, schedule):
        """ Method used by date_range to calculate the trading index.
         :param schedule: pd.DataFrame with start times in first column and end times in second column"""
        _open, _close = schedule
        # Calculate number of bars for each day
        num_bars = self._calc_num_bars(schedule)

        # ---> calculate the desired timeseries:
        if self.closed == "left":
            opens = schedule[_open].repeat(num_bars)   # keep as is
            time_series = (opens.groupby(opens.index).cumcount()) * self.frequency + opens
        elif self.closed == "right":
            opens = schedule[_open].repeat(num_bars)   # dont add row but shift up
            time_series = (opens.groupby(opens.index).cumcount()+ 1) * self.frequency + opens
        else:
            num_bars += 1
            opens = schedule[_open].repeat(num_bars)   # add row but dont shift up
            time_series = (opens.groupby(opens.index).cumcount()) * self.frequency + opens

        if not self.force_close is None:
            time_series = time_series[time_series.le(schedule[_close].repeat(num_bars))]
            if self.force_close:
                time_series = pd.concat([time_series, schedule[_close]]
                                        ).drop_duplicates().sort_values()
        return time_series

    def __call__(self, schedule, frequency, closed='right', force_close=True, **kwargs):
        """
        See class docstring for more information.

        :param schedule: schedule of a calendar, which may or may not include break_start and break_end columns
        :param frequency: frequency string that is used by pd.Timedelta to calculate the timestamps
            this must be "1D" or higher
        :param closed: the way the intervals are labeled
            'right': use the end of the interval
            'left': use the start of the interval
            None: (or 'both') use the end of the interval but include the start of the first interval
        :param force_close: how the last value of a trading session is handled
            True: guarantee that the close of the trading session is the last value
            False: guarantee that there is no value greater than the close of the trading session
            None: leave the last value as it is calculated based on the closed parameter
        :param kwargs: unused. Solely for compatibility.
        """
        self.__init__(schedule, frequency, closed, force_close)
        if self.has_breaks:
            if self._overlap_danger:
                self._check_overlap(schedule[self.before], schedule["break_end"])
                self._check_overlap(schedule[self.after], schedule["market_open"].shift(-1))

            time_series = pd.concat([ self._calc_time_series(schedule[self.before]),
                                      self._calc_time_series(schedule[self.after]) ]).sort_values()
        else:
            if self._overlap_danger:
                self._check_overlap(schedule, schedule["market_open"].shift(-1))
            time_series = self._calc_time_series(schedule)

        if self._overlap_danger: time_series = time_series.drop_duplicates()
        time_series.name = None
        return pd.DatetimeIndex(time_series, tz= "UTC")

date_range = _date_range()

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
