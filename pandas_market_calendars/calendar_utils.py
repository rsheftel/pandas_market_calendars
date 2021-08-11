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
    This is a callable class that should be used by calling the already initiated instance: `date_range`.
    Given a schedule, it will return a DatetimeIndex with all of the valid datetime at the frequency given.
    The schedule values are assumed to be in UTC.

    Signature:
    .__call__(self, schedule, frequency, closed='right', force_close=True, **kwargs)

    :param schedule: schedule of a calendar, which may or may not include break_start and break_end columns
    :param frequency: frequency string that is used by pd.Timedelta to calculate the timestamps
        this must be "1D" or higher frequency
    :param closed: the way the intervals are labeled
        'right': use the end of the interval
        'left': use the start of the interval
        None: (or 'both') use the end of the interval but include the start of the first interval (the open)
    :param force_close: how the last value of a trading session is handled
        True: guarantee that the close of the trading session is the last value
        False: guarantee that there is no value greater than the close of the trading session
        None: leave the last value as it is calculated based on the closed parameter
    :param kwargs: unused. Solely for compatibility.

    Caveats:
     * A trading session is either from market_open to market_close, or, if break_start and break_end are provided,
       from market_open to break_start and from break_end to market_close.
       The calculation based on frequency, closed and force_close is made for each trading session.
       So break_start is considered the close of the first session of a trading day
       and break_end is considered the open of the second session of the trading day.

     * If the difference between start and end of a trading session is smaller than frequency
       and closed= "right" and force_close = False, the whole session will disappear.
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
                self.has_breaks = True


    def _check_overlap(self, schedule, limit):
        """checks if calculated end times would overlap with the next start times.
        :param schedule: pd.DataFrame with start times in first column and end times in second column
        :param limit: next start time"""
        num_bars = self._calc_num_bars(schedule)
        end_times = schedule.iloc[:, 0] + num_bars * self.frequency
        if end_times.gt(limit).any():
            raise ValueError(f"The chosen frequency will lead to overlaps in the calculated index. "
                             f"Either choose a higher frequency or avoid setting force_close to None "
                             f"when setting closed to 'right', 'both' or None.")

    def _calc_num_bars(self, schedule):
        """calculate the number of timestamps needed for each trading session.
        :param schedule: pd.DataFrame with start times in first column and end times in second column
        :return: pd.Series of float64"""
        num_bars = (schedule.iloc[:, 1] - schedule.iloc[:, 0]) / self.frequency
        remains = num_bars % 1    # round up, np.ceil-style
        return num_bars.where(remains == 0, num_bars + 1 - remains).round()

    def _calc_time_series(self, schedule):
        """Method used by date_range to calculate the trading index.
         :param schedule: pd.DataFrame with start times in first column and end times in second column
         :return: pd.Series of datetime64[ns, UTC]"""
        _open, _close = schedule
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
                time_series = pd.concat([time_series, schedule[_close]]).sort_values()

        return time_series

    def __call__(self, schedule, frequency, closed='right', force_close=True, **kwargs):
        """
        See class docstring for more information.

        :param schedule: schedule of a calendar, which may or may not include break_start and break_end columns
        :param frequency: frequency string that is used by pd.Timedelta to calculate the timestamps
            this must be "1D" or higher frequency
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

        time_series.name = None
        return pd.DatetimeIndex(time_series.drop_duplicates(), tz= "UTC")

date_range = _date_range()
