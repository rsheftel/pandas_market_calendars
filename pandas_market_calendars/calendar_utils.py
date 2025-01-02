"""
Utilities to use with market_calendars
"""

import itertools
from typing import Iterable, Literal, Optional, Tuple, Union
import warnings

from re import split
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
    Warning thrown when date_range is called with a timestep that is larger than an entire session
    resulting in the session disappearing from the DatetimeIndex.

    Only an issue when closed='right' and force_close = False/None
    """


class DisappearingSessionWarning(DateRangeWarning):
    """
    Warning thrown when date_range is called with a timestep that is larger than an entire session
    resulting in the session disappearing from the DatetimeIndex.

    Only an issue when closed='right', 'both' or None and force_close = False/None
    """


class MissingSessionWarning(DateRangeWarning):
    """
    Warning thrown when a date_range() call is made with a requested session,
    but lacks the necessary columns.

    e.g. 'pre' Session requested and schedule lacks 'pre' and/or 'market_open' column
    """


class InsufficientScheduleWarning(DateRangeWarning):
    """
    Warning thrown when a date_range() call is made with a requested number of periods,
    or start-date / end-date that exceed what was provided in the given schedule
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


def missing_sessions(err: MissingSessionWarning) -> set[SESSIONS]:
    "Return the Missing Sessions from a 'MissingSessionWarning' Error Message"
    return set(split(r"[{|}]", err.args[0].replace("'", ""))[1].split(", "))  # type: ignore


def missing_columns(err: MissingSessionWarning) -> set[MKT_TIMES]:
    "Return the Missing Columns from a 'MissingSessionWarning' Error Message"
    return set(split(r"[{|}]", err.args[0].replace("'", ""))[3].split(", "))  # type: ignore


def date_range(
    schedule: pd.DataFrame,
    frequency: Union[str, pd.Timedelta, int],
    closed: Optional[Literal["left", "right", "both"]] = "right",
    force_close: Optional[bool] = True,
    session: Union[SESSIONS, Iterable[SESSIONS]] = {"RTH"},
    merge_adjacent: bool = True,
) -> pd.DatetimeIndex:
    """
    Returns a DatetimeIndex from the Start-Date to End-Date of the schedule at the desired frequency.

    CAVEATS:
        * Only "market_open", "market_close" (and, optionally, "break_start" and "break_end")
        are considered, other market times are not yet supported.

        * Timeframes Higher than "1D" are not yet supported.

        * If the difference between start and end of a trading session is smaller than an interval
        of the frequency, closed= "right" and force_close = False, the whole session will disappear.
        This will also raise a warning.

    :param schedule: Schedule of a calendar, which may or may not include break_start, break_end, pre, or post columns

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
    # ---- ---- Error Check Inputs ---- ----
    if closed not in ("left", "right", "both", None):
        raise ValueError("closed must be 'left', 'right', 'both' or None.")
    if force_close not in (True, False, None):
        raise ValueError("force_close must be True, False or None.")
    if merge_adjacent not in (True, False):
        raise ValueError("merge_adjacent must be True or False")

    # ---- ---- Standardize Frequency Param ---- ----
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

    time_series = _calc_time_series(session_times, frequency, closed, force_close)
    time_series.name = None

    first_col = schedule[session_list[0][0]]  # copy dtype info from schedule
    return pd.DatetimeIndex(
        time_series.drop_duplicates(), tz=first_col.dt.tz, dtype=first_col.dtype
    )


# region ------------------ Date Range Support Functions ------------------


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
                "while closed = 'right' and force_close = False. This will make those trading sessions "
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


def _check_disappearing_session(session_times, timestep):
    if (session_times.end - session_times.start).lt(timestep).any():
        warnings.warn(
            "An interval of the chosen frequency is larger than some of the trading sessions, "
            "while closed == 'right' and force_close is False. This will make those trading sessions "
            "disappear. Use a higher frequency or change the values of closed/force_close, to "
            "keep this from happening.",
            category=DisappearingSessionWarning,
        )


def _num_bars_ltf(session_times, timestep, closed) -> pd.Series:
    "Calculate the number of timestamps needed for each trading session."
    if closed in ("both", None):
        return np.ceil((session_times.end - session_times.start) / timestep) + 1
    else:
        return np.ceil((session_times.end - session_times.start) / timestep)


def _calc_time_series(session_times, timestep, closed, force_close) -> pd.Series:
    "Interpolate each session into a datetime series at the desired frequency."
    num_bars = _num_bars_ltf(session_times, timestep, closed)
    starts = session_times.start.repeat(num_bars)

    if closed == "right":
        # Right side of addition is cumulative time since session start in multiples of timestep
        time_series = starts + (starts.groupby(starts.index).cumcount() + 1) * timestep
    else:
        time_series = starts + (starts.groupby(starts.index).cumcount()) * timestep

    if force_close is not None:
        # Trim off all timestamps that stretched beyond their intended session
        time_series = time_series[time_series.le(session_times.end.repeat(num_bars))]

        if force_close:
            time_series = pd.concat([time_series, session_times.end]).sort_values()  # type: ignore

    return time_series


# endregion
