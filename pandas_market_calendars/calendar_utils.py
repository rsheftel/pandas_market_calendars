"""
Utilities to use with market_calendars
"""

import itertools
from math import ceil, floor
from typing import Iterable, Literal, Tuple, Union
import warnings

from re import finditer, split
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


def date_range_htf():
    "Returns a Datetime Index from the start-date to End-Date for Timeperiods of 1D and Higher"


# region ---- ---- ---- Date Range Warning Types ---- ---- ----
class DateRangeWarning(UserWarning):
    "Super Class to all Date_range Warning Types"


class OverlappingSessionWarning(DateRangeWarning):
    """
    Warning thrown when date_range is called with a timedelta that is larger than the
    gap between two sessions leading to them overlapping.
    This is only an issue when closed='right'/'both'/None and force_close=None

    For Example, the following raises a warning because the 10:00 Timestamp that is from the 'pre'
    session comes after the start of the 9:30 'RTH' session, but belongs to the 'pre' session
        >>> date_range(NYSE, '2h', 'right', None, {'pre', 'RTH'}, merge_adjacent = False)
        >>> ['2020-01-02 06:00:00', '2020-01-02 08:00:00',
             '2020-01-02 10:00:00', '2020-01-02 11:30:00',
             '2020-01-02 13:30:00', '2020-01-02 15:30:00',
             '2020-01-02 17:30:00'],
    This is particularly convoluted when close='both'/None
        >>> date_range(NYSE, '2h', 'both', None, {'pre', 'RTH'}, merge_adjacent = False)
        >>> ['2020-01-02 04:00:00' (pre), '2020-01-02 06:00:00' (pre),
             '2020-01-02 08:00:00' (pre), '2020-01-02 09:30:00' (rth),
             '2020-01-02 10:00:00' (pre), '2020-01-02 11:30:00' (rth),
             '2020-01-02 13:30:00' (rth), '2020-01-02 15:30:00' (rth),
             '2020-01-02 17:30:00' (rth)],
    """


class DisappearingSessionWarning(DateRangeWarning):
    """
    Warning thrown when date_range is called with a timedelta that is larger than an entire session
    resulting in the session disappearing from the DatetimeIndex.

    Only an issue when closed='right' and force_close = False
    """


class MissingSessionWarning(DateRangeWarning):
    """
    Warning thrown when a date_range() call is made with a requested session,
    but lacks the necessary columns. When this warning is ignored the returned
    datetimeindex will simply lack the relevant sessions

    e.g. 'pre' Session requested and schedule lacks 'pre' and/or 'market_open' column
    """


class InsufficientScheduleWarning(DateRangeWarning):
    """
    Warning thrown when a date_range() call is made with a requested number of periods,
    or start-date / end-date that exceed what was provided in the given schedule.

    If a Schedule has an insufficient start and end date then this warning is thrown twice.

    If this warning is thrown when date_range is called with a number of desired periods, then
    the desired start/end date is an approximate value. This 'approximation' is biased to
    overestimate the needed start/end time by about 1 week. This is done to limit the edge
    cases where this warning could get thrown multiple times in a row.
    """


# endregion


def filter_date_range_warnings(
    action: Literal["error", "ignore", "always", "default", "once"],
    source: Union[
        Iterable[type[DateRangeWarning]], type[DateRangeWarning]
    ] = DateRangeWarning,
):
    """
    Adjust the behavior of the date_range() warnings to the desired action.

    :param action: - The desired change to the warning behavior
        'error': Escalate Warnings into Errors
        'ignore': Silence Warning Messages
        'once': Only display a message of the given category once
        'default': Reset the behavior of the given warning category
        'always': Always show the Warning of a given category

    :param source: - The Category/Categories to apply the action to. Can be a single Warning or a list of warnings
        default: DateRangeWarning (All Warnings)
        Warning Types: MissingSessionWarning, OverlappingSessionWarning,
            DisappearingSessionWarning, InsufficientScheduleWarning
    """
    if not isinstance(source, Iterable):
        warnings.filterwarnings(action, category=source)
        return

    for src in source:
        warnings.filterwarnings(action, category=src)


SESSIONS = Literal[
    "pre",
    "post",
    "RTH",
    "pre_break",
    "post_break",
    "ETH",
    "break",
    "closed",
    "closed_masked",
]
MKT_TIMES = Literal[
    "pre", "post", "market_open", "market_close", "break_start", "break_end"
]


def parse_missing_session_warning(
    err: MissingSessionWarning,
) -> Tuple[set[SESSIONS], set[MKT_TIMES]]:
    """
    Parses a Missing Session Warning's Error Message.
    :returns Tuple[set[str], set[str]]:
        Set #1: The Missing Sessions
        Set #2: The Missing Schedule Columns
    """
    splits = split(r"[{|}]", err.args[0].replace("'", ""))
    return (set(splits[1].split(", ")), set(splits[3].split(", ")))  # type: ignore


def parse_insufficient_schedule_warning(
    err: InsufficientScheduleWarning,
) -> Tuple[bool, pd.Timestamp, pd.Timestamp]:
    """
    Parses the information from an Insufficient Schedule Warning.
    :returns Tuple[bool, pd.Timestamp, pd.Timestamp]:
        bool: True == Range is missing from the start, False == Range missing from the end
        Timestamp 1: Start of missing range
        Timestamp 2: End of the missing range.
        Note: The Timestamps are always ordered (t1 <= t2) and do not overlap with the original schedule.
        If a supplemental schedule is generated it can be concatenated on without any overlapping indices.
        data
    """
    matcher = finditer(r"\d{4}-\d{2}-\d{2}", err.args[0])
    b = "Start-Time" in err.args[0]
    t1 = pd.Timestamp(next(matcher).group())
    t2 = pd.Timestamp(next(matcher).group())

    if b:
        t2 -= pd.Timedelta("1D")
    else:
        t2 += pd.Timedelta("1D")

    return (b, t1, t2) if t1 <= t2 else (b, t2, t1)


def date_range(
    schedule: pd.DataFrame,
    frequency: Union[str, pd.Timedelta, int, float],
    closed: Union[Literal["left", "right", "both"], None] = "right",
    force_close: Union[bool, None] = True,
    session: Union[SESSIONS, Iterable[SESSIONS]] = {"RTH"},
    merge_adjacent: bool = True,
    start: Union[str, pd.Timestamp, int, float, None] = None,
    end: Union[str, pd.Timestamp, int, float, None] = None,
    periods: Union[int, None] = None,
) -> pd.DatetimeIndex:
    """
    Returns a DatetimeIndex from the Start-Date to End-Date of the schedule at the desired frequency.

    WARNINGS SYSTEM:
        *There are multiple edge-case warnings that are thrown by this function. See the Docstrings
        of each warning for more info. (DateRangeWarning, InsufficientScheduleWarning,
        MissingSessionWarning, OverlappingSessionWarning, DisappearingSessionWarning)

        *The thrown warnings can be ignored or escalated into catchable errors by using the
        filter_date_range_warnings() function.

        parse_missing_session_warning() & parse_insufficient_schedule_warning() exist to easily
        process the warnings those warnings if they are escalated into errors.

    PARAMETERS:

    :param schedule: Schedule of a calendar which includes all the columns necessary
        for the desired sessions

    :param frequency: String, Int/float (seconds) or pd.Timedelta that represents the desired
        interval of the date_range. Intervals larger than 1D are not supported.

    :param closed: the way the intervals are labeled
        'right': use the end of the interval
        'left': use the start of the interval
        None / 'both': use the end of the interval but include the start of the first interval

    :param force_close: How the last value of a trading session is handled
        True: guarantee that the close of the trading session is the last value
        False: guarantee that there is no value greater than the close of the trading session
        None: leave the last value as it is calculated based on the closed parameter

    :param session: A str representing a single session or an Iterable of the following Sessions.
        RTH: The Default Option. This is [Market_open, Market_close], if the schedule includes a
            break then the break is excluded from the returned datetime index.
        ETH: [pre, market_open] & [market_close, post]
        pre: [pre, market_open]
        post: [market_close, post]
        break: [break_start, break_end]
        pre_break: [market_open, break_start]
        post_break: [break_end, market_close]
        closed: [market_close, market_open (of the next day)] If ETH market times are given then
            this will be [post, pre (of the next day)] instead. The last session will end at
            Midnight of the timezone the schedule is given in.
        closed_masked: Same as closed, but Weekends & Holidays are ignored. Instead, the Datetime
            index stops at Midnight on the trading day before the break and resumes at midnight
            prior to the next trading day. **Note: This is Midnight of the Timezone the schedule is
            given in, not Midnight of the exchange's tz since the exchange's tz is not known.

    :param merge_adjacent: Bool representing if adjacent sessions should be merged into a single session.
        For Example, NYSE w/ session={'RTH', 'ETH'}, frequency=2h, closed=left, force_close=False
        merge_adjacent == True => [pre, post]
            >>> ['2020-01-02 04:00:00', '2020-01-02 06:00:00',
                 '2020-01-02 08:00:00', '2020-01-02 10:00:00',
                 '2020-01-02 12:00:00', '2020-01-02 14:00:00',
                 '2020-01-02 16:00:00', '2020-01-02 18:00:00']
        merge_adjacent == False => [pre, market_open] & [market_open, market_close] & [market_close, post]
            >>> ['2020-01-02 04:00:00', '2020-01-02 06:00:00',
                 '2020-01-02 08:00:00', '2020-01-02 09:30:00',
                 '2020-01-02 11:30:00', '2020-01-02 13:30:00',
                 '2020-01-02 15:30:00', '2020-01-02 16:00:00',
                 '2020-01-02 18:00:00']
        merge_adjacent=False re-aligns the timestamps to the session, but this results in
        the difference between timestamps not always equaling the desired frequency.

    :param start: Optional [String, Int/float (POSIX seconds) or pd.Timestamp] of the desired start time.
        :If left as None then the start-time of the the Schedule is used.
        :If no TZ info is given it will be interpreted in the same timezone as the first column
        of the schedule
        :Start can be a Day and Time, but the returned index will still be aligned to the underlying
        schedule. e.g. Session = [9:30am, 12pm], frequency=7min, start=9:45am. Underlying session
         = [9:30, 9:37, 9:44, 9:51, ...] => returned DatetimeIndex = [9:51, ...]

    :param end: Optional [String, Int/float (POSIX seconds) or pd.Timestamp] of the desired end time.
        :If left as None then the end-time of the the Schedule is used.
        :If no TZ info is given it will be interpreted in the same timezone as the first column
        **Note: The time given is an absolute value. i.e. end="2020-01-01" == "2020-01-01 00:00"
        returning times prior to Midnight of "2019-12-31", not to the EOD of "2020-01-01"

    :param periods: Optional Integer number of periods to return. If a Period count, Start time,
        and End time are given the period count is ignored.
        None: Period count is ignored. Returned index is all periods in [Start, End]
        Int: # of periods to return. By default, this is the first N periods following the start.
            If an end time is given then this is the N periods prior to the End Time (inclusive).
        CAVEAT: When Force_close == False & closed == 'right'/'both' the number of periods returned
            may be less than the parameter given.

    :return: pd.DatetimeIndex of datetime64[ns, TZ-Aware]
    """
    # ---- ---- Error Check Inputs ---- ----
    if closed not in ("left", "right", "both", None):
        raise ValueError("closed must be 'left', 'right', 'both' or None.")
    if force_close not in (True, False, None):
        raise ValueError("force_close must be True, False or None.")
    if merge_adjacent not in (True, False):
        raise ValueError("merge_adjacent must be True or False")

    # ---- ---- Standardize Frequency Param ---- ----
    if isinstance(frequency, (int, float)):
        frequency = int(frequency * 1_000_000_000)
    try:
        frequency = pd.Timedelta(frequency)
    except ValueError as e:
        raise ValueError(f"Market Calendar Date_range Timeframe Error: {e}") from e
    if frequency <= pd.Timedelta("0s"):
        raise ValueError("Market Calendar Date_Range Frequency must be Positive.")
    if frequency > pd.Timedelta("1D"):
        raise ValueError(
            "Market Calendar Date_Range Frequency Cannot Be longer than '1D'."
        )

    session_list, mask = _make_session_list(
        set(schedule.columns), session, merge_adjacent
    )
    if len(session_list) == 0:
        return pd.DatetimeIndex([], dtype="datetime64[ns, UTC]")

    session_times = _reconfigure_schedule(schedule, session_list, mask)
    # Trim off all 0 length sessions
    session_times = session_times[session_times.start.ne(session_times.end)]
    _error_check_sessions(session_times, frequency, closed, force_close)

    tz = schedule[session_list[0][0]].dt.tz  # copy tz info from schedule
    dtype = schedule[session_list[0][0]].dtype  # copy dtype info from schedule
    start, end, periods = _standardize_times(schedule, start, end, periods, tz)

    time_series = _calc_time_series(
        session_times, frequency, closed, force_close, start, end, periods
    )
    time_series.name = None

    return pd.DatetimeIndex(time_series, tz=tz, dtype=dtype)


# region ------------------ Date Range Subroutines ------------------


def _make_session_list(
    columns: set, sessions: Union[str, Iterable], merge_adjacent: bool
) -> Tuple[list, bool]:
    "Create a list of (Session Start, Session End) Tuples"
    session_times = []
    missing_cols = set()
    missing_sess = set()
    sessions = {sessions} if isinstance(sessions, str) else set(sessions)

    if len(extras := sessions.difference(set(SESSIONS.__args__))) > 0:  # type: ignore
        raise ValueError(f"Unknown Date_Range Market Session: {extras}")

    if "ETH" in sessions:  # Standardize ETH to 'pre' and 'post'
        sessions = sessions - {"ETH"} | {"pre", "post"}
    if "closed_masked" in sessions:  # closed_masked == 'closed' for this step
        sessions |= {"closed"}
    if "pre" in columns:  # Add wrap-around sessions
        columns |= {"pre_wrap"}
    if "market_open" in columns:
        columns |= {"market_open_wrap"}

    def _extend_statement(session, parts):
        if session not in sessions:
            return
        if columns.issuperset(parts):
            session_times.extend(parts)
        else:
            missing_sess.update({session})
            missing_cols.update(set(parts) - columns)

    # Append session_start, session_end for each desired session *in session order*
    _extend_statement("pre", ("pre", "market_open"))
    if {"break_start", "break_end"}.issubset(columns):
        # If the schedule has breaks then sub-divide RTH into pre & post break sessions
        if "RTH" in sessions:
            sessions = sessions - {"RTH"} | {"pre_break", "post_break"}
        _extend_statement("pre_break", ("market_open", "break_start"))
        _extend_statement("break", ("break_start", "break_end"))
        _extend_statement("post_break", ("break_end", "market_close"))
    else:
        _extend_statement("RTH", ("market_open", "market_close"))
    _extend_statement("post", ("market_close", "post"))

    # Closed can mean [close, open], [close, pre], [pre, post], or [post, open] Adjust accordingly
    s_start = "post" if "post" in columns else "market_close"
    s_end = "pre_wrap" if "pre" in columns else "market_open_wrap"
    _extend_statement("closed", (s_start, s_end))

    if len(missing_sess) > 0:
        warnings.warn(
            f"Requested Sessions: {missing_sess}, but schedule is missing columns: {missing_cols}."
            "\nResulting DatetimeIndex will lack those sessions. ",
            category=MissingSessionWarning,
        )

    if merge_adjacent:
        drop_set = set()
        for i in range(1, len(session_times) - 1, 2):
            if session_times[i] == session_times[i + 1]:
                drop_set |= {session_times[i]}

        # Guaranteed to drop in pairs => no check needed before zipping
        session_times = [t for t in session_times if t not in drop_set]

    # Zip the flat list into a list of pairs
    session_pairs = list(zip(*(iter(session_times),) * 2))

    return session_pairs, "closed_masked" in sessions


def _standardize_times(
    schedule, start, end, periods, tz
) -> Tuple[pd.Timestamp, pd.Timestamp, Union[int, None]]:
    "Standardize start and end into a timestamp of the relevant timezone"
    if all((start, end, periods)):
        periods = None  # Ignore Periods if all 3 params are given.

    if start is not None:
        if isinstance(start, (int, float)):
            start *= 1_000_000_000
        try:
            start = pd.Timestamp(start)
            if start.tz is None:
                start = start.tz_localize(tz)
        except ValueError as e:
            raise ValueError(f"Invalid Time ({start = }) given to date_range()") from e

        if start < schedule.index[0].tz_localize(tz):
            warnings.warn(
                f"Insufficient Schedule. Requested Start-Time: {start.normalize().tz_localize(None)}. "
                f"Schedule starts at: {schedule.index[0].normalize().tz_localize(None)}",
                category=InsufficientScheduleWarning,
            )

    if end is not None:
        if isinstance(end, (int, float)):
            end *= 1_000_000_000
        try:
            end = pd.Timestamp(end)
            if end.tz is None and tz is not None:
                end = end.tz_localize(tz)
        except ValueError as e:
            raise ValueError(f"Invalid Time ({end = }) given to date_range()") from e

        if end > schedule.index[-1].tz_localize(tz) + pd.Timedelta("1D"):
            # Checking against the day and not the specific session since so requesting a time
            # after the last session's close but before the next day doesn't throw a warning.
            requested_end = end.normalize().tz_localize(None) - pd.Timedelta("1D")
            warnings.warn(
                f"Insufficient Schedule. Requested End-Time: {requested_end}. "
                f"Schedule ends at: {schedule.index[-1].normalize().tz_localize(None)}",
                category=InsufficientScheduleWarning,
            )

    if start is not None and end is not None and start > end:
        raise ValueError(
            "Date_range() given a start-date that occurs after the given end-date. "
            f"{start = }, {end = }"
        )

    return start, end, periods


def _reconfigure_schedule(schedule, session_list, mask_close) -> pd.DataFrame:
    "Reconfigure a schedule into a sorted dataframe of [start, end] times for each session"

    sessions = []

    for start, end in session_list:
        if not end.endswith("_wrap"):
            # Simple Session where 'start' occurs before 'end'
            sessions.append(
                schedule[[start, end]]
                .rename(columns={start: "start", end: "end"})
                .set_index("start", drop=False)
            )
            continue

        # 'closed' Session that wraps around midnight. Shift the 'end' col by 1 Day
        end = end.rstrip("_wrap")
        tmp = pd.DataFrame(
            {
                "start": schedule[start],
                "end": schedule[end].shift(-1),
            }
        ).set_index("start", drop=False)

        # Shift(-1) leaves last index of 'end' as 'NaT'
        # Set the [-1, 'end' ('end' === 1)] cell to Midnight of the 'start' time of that row.
        tmp.iloc[-1, 1] = tmp.iloc[-1, 0].normalize() + pd.Timedelta("1D")  # type: ignore

        if mask_close:
            # Do some additional work to split 'closed' sessions that span weekends/holidays
            sessions_to_split = tmp["end"] - tmp["start"] > pd.Timedelta("1D")

            split_strt = tmp[sessions_to_split]["start"]
            split_end = tmp[sessions_to_split]["end"]

            sessions.append(
                pd.DataFrame(  # From start of the long close to Midnight
                    {
                        "start": split_strt,
                        "end": split_strt.dt.normalize() + pd.Timedelta("1D"),
                    }
                ).set_index("start", drop=False)
            )
            sessions.append(
                pd.DataFrame(  # From Midnight to the end of the long close
                    {
                        "start": split_end.dt.normalize(),
                        "end": split_end,
                    }
                ).set_index("start", drop=False)
            )

            # leave tmp as all the sessions that were not split
            tmp = tmp[~sessions_to_split]

        sessions.append(tmp)

    return pd.concat(sessions).sort_index()


def _error_check_sessions(session_times, timestep, closed, force_close):
    if session_times.start.gt(session_times.end).any():
        raise ValueError(
            "Desired Sessions from the Schedule contain rows where session start < session end, "
            "please correct the schedule"
        )

    # Disappearing Session
    if force_close is False and closed == "right":
        # only check if needed
        if (session_times.end - session_times.start).lt(timestep).any():
            warnings.warn(
                "An interval of the chosen frequency is larger than some of the trading sessions, "
                "while closed='right' and force_close=False. This will make those trading sessions "
                "disappear. Use a higher frequency or change the values of closed/force_close, to "
                "keep this from happening.",
                category=DisappearingSessionWarning,
            )

    # Overlapping Session
    if force_close is None and closed != "left":
        num_bars = _num_bars_ltf(session_times, timestep, closed)
        end_times = session_times.start + num_bars * timestep

        if end_times.gt(session_times.start.shift(-1)).any():
            warnings.warn(
                "The desired frequency results in date_range() generating overlapping sessions. "
                "This can happen when the timestep is larger than a session, or when "
                "merge_session = False and a session is not evenly divisible by the timestep. "
                "The overlapping timestep can be deleted with force_close = True or False",
                category=OverlappingSessionWarning,
            )


def _num_bars_ltf(session_times, timestep, closed) -> pd.Series:
    "Calculate the number of timestamps needed for each trading session."
    if closed in ("both", None):
        return np.ceil((session_times.end - session_times.start) / timestep) + 1
    else:
        return np.ceil((session_times.end - session_times.start) / timestep)


def _course_trim_to_period_count(num_bars, periods, reverse) -> pd.Series:
    """
    Course Trim the Session times to the desired period count.
    Large enough of a sub-routine to merit its own function call.
    """
    if reverse:
        # If end-date is given calculate sum in reverse order
        num_bars = num_bars[::-1]

    _sum = num_bars.cumsum()

    if _sum.iloc[-1] < periods:
        # Insufficient Number of Periods. Try to estimate an ending time from the data given.
        # delta = (end_date - start_date) / (cumulative # of periods) * (periods still needed) * fudge factor
        delta = abs(
            # (end_date - start_date) / (cumulative # of periods)
            ((_sum.index[-1] - _sum.index[0]) / _sum.iloc[-1])
            * (periods - _sum.iloc[-1])  # (periods still needed)
            * 1.05  # (Fudge Factor for weekends/holidays)
        )
        # delta = math.ceil(delta) + '1W'
        delta = (delta // pd.Timedelta("1D") + 8) * pd.Timedelta("1D")
        # The 1.05 Factor handles when the schedule is short by a few months, the + '1W' handles
        # when the schedule is short by only a few periods. While 1 Week is absolute overkill,
        # generating the extra few days is very little extra cost compared to throwing this error
        # a second or even third time.

        if reverse:
            approx_start = _sum.index[-1] - delta
            warnings.warn(
                f"Insufficient Schedule. Requested Approx Start-Time: {approx_start}. "
                f"Schedule starts at: {_sum.index[-1].normalize().tz_localize(None)}",
                category=InsufficientScheduleWarning,
            )
        else:
            approx_end = _sum.index[-1] + delta
            warnings.warn(
                f"Insufficient Schedule. Requested Approx End-Time: {approx_end}. "
                f"Schedule ends at: {_sum.index[-1].normalize().tz_localize(None)}",
                category=InsufficientScheduleWarning,
            )

    sessions_to_keep = _sum < periods
    # Shifting Ensures the number of needed periods are generated, but no more.
    sessions_to_keep = sessions_to_keep.shift(1, fill_value=True)

    if reverse:
        # If end-date is given calculate un-reverse the order of the series
        sessions_to_keep = sessions_to_keep[::-1]

    return sessions_to_keep


def _calc_time_series(
    session_times, timestep, closed, force_close, start, end, periods
) -> pd.Series:
    "Interpolate each session into a datetime series at the desired frequency."
    # region ---- ---- ---- Trim the Sessions ---- ---- ----
    # Compare 'start' to the session end times so that if 'start' is in the middle of a session
    # that session remains in session_times. Vise-vera for End
    if start is not None:
        session_times = session_times[session_times.end > start]
    if end is not None:
        session_times = session_times[session_times.start < end]
    if len(session_times) == 0:
        return pd.Series([])

    # Override the First Session's Start and Last Session's End times if needed
    if start is not None and start > session_times.loc[session_times.index[0], "start"]:
        # Align the start to a multiple of the timestep after the session's beginning.
        # This is to make the returned DTIndex consistent across all start/end/period settings.
        session_start = session_times.loc[session_times.index[0], "start"]
        start_aligned = session_start + (
            ceil((start - session_start) / timestep) * timestep
        )
        session_times.loc[session_times.index[0], "start"] = start_aligned
    if end is not None and end < session_times.loc[session_times.index[-1], "end"]:
        session_start = session_times.loc[session_times.index[0], "start"]
        end_aligned = session_start + (
            floor((end - session_start) / timestep) * timestep
        )
        session_times.loc[session_times.index[-1], "end"] = end_aligned

    num_bars = _num_bars_ltf(session_times, timestep, closed)

    if periods is not None:
        sessions_to_keep = _course_trim_to_period_count(
            num_bars, periods, end is not None
        )
        num_bars = num_bars[sessions_to_keep]
        session_times = session_times[sessions_to_keep]

    # endregion

    starts = session_times.start.repeat(num_bars)  # type: ignore

    if closed == "right":
        # Right side of addition is cumulative time since session start in multiples of timestep
        time_series = starts + (starts.groupby(starts.index).cumcount() + 1) * timestep
    else:
        time_series = starts + (starts.groupby(starts.index).cumcount()) * timestep

    if force_close is not None:
        # Trim off all timestamps that stretched beyond their intended session
        time_series = time_series[time_series.le(session_times.end.repeat(num_bars))]

        if force_close:
            time_series = pd.concat([time_series, session_times.end])

    time_series = time_series.drop_duplicates().sort_values()  # type: ignore

    if periods is not None and len(time_series) > 0:
        # Although likely redundant, Fine Trim to desired period count.
        if end is not None:
            s_len = len(time_series)
            time_series = time_series[max(s_len - periods, 0) : s_len]
        else:
            time_series = time_series[0:periods]

    return time_series


# endregion
