"""
Utilities to use with market_calendars
"""

import itertools
import warnings

import numpy as np
import pandas as pd


def merge_schedules(schedules, how="outer"):
    """
    Given a list of schedules will return a merged schedule. The merge method (how) will either return the superset
    of any datetime when any schedule is open (outer) or only the datetime where all markets are open (inner)

    CAVEATS:
        * This does not work for schedules with breaks, the break information will be lost.
        * Only "market_open" and "market_close" are considered, other market times are not yet supported.

    :param schedules: list of schedules
    :param how: outer or inner
    :return: schedule DataFrame
    """
    all_cols = [x.columns for x in schedules]
    all_cols = list(itertools.chain(*all_cols))
    if ("break_start" in all_cols) or ("break_end" in all_cols):
        warnings.warn(
            "Merge schedules will drop the break_start and break_end from result."
        )

    result = schedules[0]
    for schedule in schedules[1:]:
        result = result.merge(schedule, how=how, right_index=True, left_index=True)
        if how == "outer":
            result["market_open"] = result.apply(
                lambda x: min(x.market_open_x, x.market_open_y), axis=1
            )
            result["market_close"] = result.apply(
                lambda x: max(x.market_close_x, x.market_close_y), axis=1
            )
        elif how == "inner":
            result["market_open"] = result.apply(
                lambda x: max(x.market_open_x, x.market_open_y), axis=1
            )
            result["market_close"] = result.apply(
                lambda x: min(x.market_close_x, x.market_close_y), axis=1
            )
        else:
            raise ValueError('how argument must be "inner" or "outer"')
        result = result[["market_open", "market_close"]]
    return result


def convert_freq(index, frequency):
    """
    Converts a DateTimeIndex to a new lower frequency

    :param index: DateTimeIndex
    :param frequency: frequency string
    :return: DateTimeIndex
    """
    return pd.DataFrame(index=index).asfreq(frequency).index


def date_range(schedule, frequency, closed="right", force_close=True, **_):
    """
    Returns a DatetimeIndex from the Start-Date to End-Date of the schedule at the desired frequency.

    CAVEATS:
        * Only "market_open", "market_close" (and, optionally, "break_start" and "break_end")
        are considered, other market times are not yet supported.

        * Timeframes Higher than "1D" are not yet supported.

        * If the difference between start and end of a trading session is smaller than an interval
        of the frequency, closed= "right" and force_close = False, the whole session will disappear.
        This will also raise a warning.

    :param schedule: Schedule of a calendar, which may or may not include break_start and break_end columns

    :param frequency: frequency string that is used by pd.Timedelta to calculate the timestamps
        this must be "1D" or higher frequency

    :param closed: the way the intervals are labeled
        'right': use the end of the interval
        'left': use the start of the interval
        None / 'both': use the end of the interval but include the start of the first interval

    :param force_close: how the last value of a trading session is handled
        True: guarantee that the close of the trading session is the last value
        False: guarantee that there is no value greater than the close of the trading session
        None: leave the last value as it is calculated based on the closed parameter

    :return: pd.DatetimeIndex of datetime64[ns, UTC]
    """
    _error_check(schedule, closed, force_close)

    frequency = _check_frequency(frequency)
    if frequency is None:
        return pd.DatetimeIndex([], dtype="datetime64[ns, UTC]")

    if _check_breaks(schedule):
        before = schedule[["market_open", "break_start"]].set_index(
            schedule["market_open"]
        )
        after = schedule[["break_end", "market_close"]].set_index(schedule["break_end"])
        before.columns = after.columns = ["start", "end"]
        schedule = pd.concat([before, after]).sort_index()
    else:
        schedule = schedule.rename(
            columns={"market_open": "start", "market_close": "end"}
        )

    if force_close is None and closed != "left":
        _check_overlapping_session(schedule, frequency, closed)

    if force_close is False and closed == "right":
        _check_disappearing_session(schedule, frequency)

    # Drop any zero length trading sessions
    schedule = schedule[schedule.start.ne(schedule.end)]

    time_series = _calc_time_series(schedule, frequency, closed, force_close)

    time_series.name = None
    return pd.DatetimeIndex(time_series.drop_duplicates())


# region ------------------ Date Range Support Functions ------------------


def _error_check(schedule, closed, force_close):
    if closed not in ("left", "right", "both", None):
        raise ValueError("closed must be 'left', 'right', 'both' or None.")
    if force_close not in (True, False, None):
        raise ValueError("force_close must be True, False or None.")

    if schedule.market_close.lt(schedule.market_open).any():
        raise ValueError(
            "Schedule contains rows where market_close < market_open,"
            " please correct the schedule"
        )


def _check_frequency(frequency):
    frequency = pd.Timedelta(frequency)
    if frequency > pd.Timedelta("1D"):
        raise ValueError("Frequency must be 1D or higher frequency.")
    return frequency


def _check_breaks(schedule) -> bool:
    if "break_start" not in schedule:
        return False

    if not all(
        [
            schedule.market_open.le(schedule.break_start).all(),
            schedule.break_start.le(schedule.break_end).all(),
            schedule.break_end.le(schedule.market_close).all(),
        ]
    ):
        raise ValueError(
            "Not all rows match the condition: "
            "market_open <= break_start <= break_end <= market_close, "
            "please correct the schedule"
        )
    return True


def _check_overlapping_session(schedule, frequency, closed):
    """
    Checks if any end time would occur after a the next session's start time.
    Only an issue when force_close is None and closed != left.

    :param schedule: pd.DataFrame with first column: 'start' and second column: 'end'
    :raises ValueError:
    """
    num_bars = _num_bars_ltf(schedule, frequency, closed)
    end_times = schedule.start + num_bars * frequency

    if end_times.gt(schedule.start.shift(-1)).any():
        raise ValueError(
            "The chosen frequency will lead to overlaps in the calculated index. "
            "Either choose a higher frequency or avoid setting force_close to None "
            "when setting closed to 'right', 'both' or None."
        )


def _check_disappearing_session(schedule, frequency):
    """checks if requested frequency and schedule would lead to lost trading sessions.
    Only necessary when force_close = False and closed = "right".

    :param schedule: pd.DataFrame with first column: 'start' and second column: 'end'
    :raises UserWarning:"""

    if (schedule.end - schedule.start).lt(frequency).any():
        warnings.warn(
            "An interval of the chosen frequency is larger than some of the trading sessions, "
            "while closed == 'right' and force_close is False. This will make those trading sessions "
            "disappear. Use a higher frequency or change the values of closed/force_close, to "
            "keep this from happening."
        )


def _num_bars_ltf(schedule, frequency, closed):
    """calculate the number of timestamps needed for each trading session.

    :param schedule: pd.DataFrame with first column: 'start' and second column: 'end'
    :return: pd.Series of float64"""
    if closed in ("both", None):
        return np.ceil((schedule.end - schedule.start) / frequency) + 1
    else:
        return np.ceil((schedule.end - schedule.start) / frequency)


def _calc_time_series(schedule, frequency, closed, force_close):
    """Method used by date_range to calculate the trading index.

    :param schedule: pd.DataFrame with first column: 'start' and second column: 'end'
    :return: pd.Series of datetime64[ns, UTC]"""

    num_bars = _num_bars_ltf(schedule, frequency, closed)
    opens = schedule.start.repeat(num_bars)

    if closed == "right":
        time_series = (opens.groupby(opens.index).cumcount() + 1) * frequency + opens
    else:
        time_series = (opens.groupby(opens.index).cumcount()) * frequency + opens

    if force_close is not None:
        time_series = time_series[time_series.le(schedule.end.repeat(num_bars))]
        if force_close:
            time_series = pd.concat([time_series, schedule.end]).sort_values()

    return time_series


# endregion
