# Fork of zipline from Quantopian. Licensed under MIT, original licence below
#
# Copyright 2016 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import warnings
from abc import ABCMeta, abstractmethod
from datetime import time
from typing import Literal, Union

import pandas as pd
from pandas.tseries.offsets import CustomBusinessDay

from .class_registry import RegisteryMeta, ProtectedDict

from . import calendar_utils as u

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)

WEEKMASK_ABBR = {
    MONDAY: "Mon",
    TUESDAY: "Tue",
    WEDNESDAY: "Wed",
    THURSDAY: "Thu",
    FRIDAY: "Fri",
    SATURDAY: "Sat",
    SUNDAY: "Sun",
}


class DEFAULT:
    pass


class MarketCalendarMeta(ABCMeta, RegisteryMeta):
    pass


class MarketCalendar(metaclass=MarketCalendarMeta):
    """
    An MarketCalendar represents the timing information of a single market or exchange.
    Unless otherwise noted all times are in UTC and use Pandas data structures.
    """

    regular_market_times = {
        "market_open": ((None, time(0)),),
        "market_close": ((None, time(23)),),
    }

    open_close_map = {
        "market_open": True,
        "market_close": False,
        "break_start": False,
        "break_end": True,
        "pre": True,
        "post": False,
    }

    @staticmethod
    def _tdelta(t, day_offset=0):
        try:
            return pd.Timedelta(
                days=day_offset, hours=t.hour, minutes=t.minute, seconds=t.second
            )
        except AttributeError:
            t, day_offset = t
            return pd.Timedelta(
                days=day_offset, hours=t.hour, minutes=t.minute, seconds=t.second
            )

    @staticmethod
    def _off(tple):
        try:
            return tple[2]
        except IndexError:
            return 0

    @classmethod
    def calendar_names(cls):
        """All Market Calendar names and aliases that can be used in "factory"
        :return: list(str)
        """
        return [
            cal
            for cal in cls._regmeta_class_registry.keys()
            if cal not in ["MarketCalendar", "TradingCalendar"]
        ]

    @classmethod
    def factory(
        cls, name, *args, **kwargs
    ):  # Will be set by Meta, keeping it there for tests
        """
        :param name: The name of the MarketCalendar to be retrieved.
        :param *args/**kwargs: passed to requested MarketCalendar.__init__
        :return: MarketCalendar of the desired calendar.
        """
        return

    def __init__(self, open_time=None, close_time=None):
        """
        :param open_time: Market open time override as datetime.time object. If None then default is used.
        :param close_time: Market close time override as datetime.time object. If None then default is used.
        """

        self.regular_market_times = self.regular_market_times.copy()
        self.open_close_map = self.open_close_map.copy()
        self._customized_market_times = []

        if open_time is not None:
            self.change_time("market_open", open_time)

        if close_time is not None:
            self.change_time("market_close", close_time)

        if not hasattr(self, "_market_times"):
            self._prepare_regular_market_times()

    @property
    @abstractmethod
    def name(self):
        """
        Name of the market

        :return: string name
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def full_name(self):
        """
        Full name of the market

        :return: string name
        """
        return self.name

    @property
    @abstractmethod
    def tz(self):
        """
        Time zone for the market.

        :return: timezone
        """
        raise NotImplementedError()

    @property
    def market_times(self):
        return self._market_times

    def _prepare_regular_market_times(self):
        oc_map = self.open_close_map
        assert all(
            isinstance(x, bool) for x in oc_map.values()
        ), "Values in open_close_map need to be True or False"

        regular = self.regular_market_times
        discontinued = ProtectedDict()
        regular_tds = {}

        for market_time, times in regular.items():
            # in case a market_time has been discontinued, extend the last time
            # and add it to the discontinued_market_times dictionary
            if market_time.startswith("interruption_"):
                raise ValueError("'interruption_' prefix is reserved")

            if times[-1][1] is None:
                discontinued._set(market_time, times[-1][0])
                times = times[:-1]
                regular._set(market_time, times)

            regular_tds[market_time] = tuple(
                (t[0], self._tdelta(t[1], self._off(t))) for t in times
            )

        if discontinued:
            warnings.warn(
                f"{list(discontinued.keys())} are discontinued, the dictionary"
                f" `.discontinued_market_times` has the dates on which these were discontinued."
                f" The times as of those dates are incorrect, use .remove_time(market_time)"
                f" to ignore a market_time."
            )

        self.discontinued_market_times = discontinued
        self.regular_market_times = regular

        self._regular_market_timedeltas = regular_tds
        self._market_times = sorted(regular.keys(), key=lambda x: regular_tds[x][-1][1])
        self._oc_market_times = list(filter(oc_map.__contains__, self._market_times))

    def _set_time(self, market_time, times, opens):
        if isinstance(times, (tuple, list)):  # passed a tuple
            if not isinstance(times[0], (tuple, list)):  # doesn't have a tuple inside
                if times[0] is None:  # seems to be a tuple indicating starting time
                    times = (times,)
                else:  # must be a tuple with: (time, offset)
                    times = ((None, times[0], times[1]),)
        else:  # should be a datetime.time object
            times = ((None, times),)

        ln = len(times)
        for i, t in enumerate(times):
            try:
                assert (
                    t[0] is None
                    or isinstance(t[0], str)
                    or isinstance(t[0], pd.Timestamp)
                )
                assert isinstance(t[1], time) or (
                    ln > 1 and i == ln - 1 and t[1] is None
                )
                assert isinstance(self._off(t), int)
            except AssertionError:
                raise AssertionError(
                    "The passed time information is not in the right format, "
                    "please consult the docs for how to set market times"
                )

        if opens is DEFAULT:
            opens = self.__class__.open_close_map.get(market_time, None)

        if opens in (True, False):
            self.open_close_map._set(market_time, opens)

        elif opens is None:  # make sure it's ignored
            try:
                self.open_close_map._del(market_time)
            except KeyError:
                pass
        else:
            raise ValueError(
                "when you pass `opens`, it needs to be True, False, or None"
            )

        self.regular_market_times._set(market_time, times)

        if not self.is_custom(market_time):
            self._customized_market_times.append(market_time)

        self._prepare_regular_market_times()

    def change_time(self, market_time, times, opens=DEFAULT):
        """
        Changes the specified market time in regular_market_times and makes the necessary adjustments.

        :param market_time: the market_time to change
        :param times: new time information
        :param opens: whether the market_time is a time that closes or opens the market
            this is only needed if the market_time should be respected by .open_at_time
            True: opens
            False: closes
            None: consider it neither opening nor closing, don't add to open_close_map (ignore in .open_at_time)
            DEFAULT: same as None, unless the market_time is in self.__class__.open_close_map. Then it will take
                the default value as defined by the class.
        :return: None
        """
        assert market_time in self.regular_market_times, (
            f"{market_time} is not in regular_market_times:" f"\n{self._market_times}."
        )
        return self._set_time(market_time, times, opens)

    def add_time(self, market_time, times, opens=DEFAULT):
        """
        Adds the specified market time to regular_market_times and makes the necessary adjustments.

        :param market_time: the market_time to add
        :param times: the time information
        :param opens: see .change_time docstring
        :return: None
        """
        assert market_time not in self.regular_market_times, (
            f"{market_time} is already in regular_market_times:"
            f"\n{self._market_times}"
        )

        return self._set_time(market_time, times, opens)

    def remove_time(self, market_time):
        """
        Removes the specified market time from regular_market_times and makes the necessary adjustments.

        :param market_time: the market_time to remove
        :return: None
        """

        self.regular_market_times._del(market_time)
        try:
            self.open_close_map._del(market_time)
        except KeyError:
            pass

        self._prepare_regular_market_times()
        if self.is_custom(market_time):
            self._customized_market_times.remove(market_time)

    def is_custom(self, market_time):
        return market_time in self._customized_market_times

    @property
    def has_custom(self):
        return len(self._customized_market_times) > 0

    def is_discontinued(self, market_time):
        return market_time in self.discontinued_market_times

    @property
    def has_discontinued(self):
        return len(self.discontinued_market_times) > 0

    def get_time(self, market_time, all_times=False):
        try:
            times = self.regular_market_times[market_time]
        except KeyError as e:
            if "break_start" in market_time or "break_end" in market_time:
                return None  # in case of no breaks
            elif market_time in ["market_open", "market_close"]:
                raise NotImplementedError("You need to set market_times")
            else:
                raise e

        if all_times:
            return times
        return times[-1][1].replace(tzinfo=self.tz)

    def get_time_on(self, market_time, date):
        times = self.get_time(market_time, all_times=True)
        if times is None:
            return None

        date = pd.Timestamp(date)
        for d, t in times[::-1]:
            if d is None or pd.Timestamp(d) < date:
                return t.replace(tzinfo=self.tz)

    def open_time_on(self, date):
        return self.get_time_on("market_open", date)

    def close_time_on(self, date):
        return self.get_time_on("market_close", date)

    def break_start_on(self, date):
        return self.get_time_on("break_start", date)

    def break_end_on(self, date):
        return self.get_time_on("break_end", date)

    @property
    def open_time(self):
        """
        Default open time for the market

        :return: time
        """
        return self.get_time("market_open")

    @property
    def close_time(self):
        """
        Default close time for the market

        :return: time
        """
        return self.get_time("market_close")

    @property
    def break_start(self):
        """
        Break time start. If None then there is no break

        :return: time or None
        """
        return self.get_time("break_start")

    @property
    def break_end(self):
        """
        Break time end. If None then there is no break

        :return: time or None
        """
        return self.get_time("break_end")

    @property
    def regular_holidays(self):
        """

        :return: pd.AbstractHolidayCalendar: a calendar containing the regular holidays for this calendar
        """
        return None

    @property
    def adhoc_holidays(self):
        """

        :return: list of ad-hoc holidays
        """
        return []

    @property
    def weekmask(self):
        return "Mon Tue Wed Thu Fri"

    @property
    def special_opens(self):
        """
        A list of special open times and corresponding AbstractHolidayCalendar.

        :return: List of (time, AbstractHolidayCalendar) tuples
        """
        return []

    @property
    def special_opens_adhoc(self):
        """

        :return: List of (time, DatetimeIndex) tuples that represent special opens that cannot be codified into rules.
        """
        return []

    @property
    def special_closes(self):
        """
        A list of special close times and corresponding HolidayCalendars.

        :return: List of (time, AbstractHolidayCalendar) tuples
        """
        return []

    @property
    def special_closes_adhoc(self):
        """

        :return: List of (time, DatetimeIndex) tuples that represent special closes that cannot be codified into rules.
        """
        return []

    def get_special_times(self, market_time):
        return getattr(self, "special_" + market_time, [])

    def get_special_times_adhoc(self, market_time):
        return getattr(self, "special_" + market_time + "_adhoc", [])

    def get_offset(self, market_time):
        return self._off(self.get_time(market_time, all_times=True)[-1])

    @property
    def open_offset(self):
        """
        :return: open offset
        """
        return self.get_offset("market_open")

    @property
    def close_offset(self):
        """
        :return: close offset
        """
        return self.get_offset("market_close")

    @property
    def interruptions(self):
        """
        This needs to be a list with a tuple for each date that had an interruption.
        The tuple should have this layout:

            (date, start_time, end_time[, start_time2, end_time2, ...])

        E.g.:
        [
            ("2002-02-03", (time(11), -1), time(11, 2)),
            ("2010-01-11", time(11), (time(11, 1), 1)),
            ("2010-01-13", time(9, 59), time(10), time(10, 29), time(10, 30)),
            ("2011-01-10", time(11), time(11, 1))
        ]

        The date needs to be a string in this format: 'yyyy-mm-dd'.
        Times need to be two datetime.time objects for each interruption, indicating start and end.
         Optionally these can be wrapped in a tuple, where the
         second element needs to be an integer indicating an offset.
        On "2010-01-13" in the example, it is shown that there can be multiple interruptions in a day.
        """
        return []

    def _convert(self, col: pd.Series):
        """
        col is a series indexed by dates at which interruptions occurred. The values are either the start or end times
        of an interruption, represented by either a timedelta or a tuple with a timedelta and day offset of the form
        (timedelta, offset). _convert produces a new series where the values are replaced by datetimes equal to the
        index of the original series plus the offset if present, at the timedelta.

        E.g.:
        >>> self._convert(
                pd.Series(
                    [datetime.time(11, 2), (datetime.time(11, 1), 1), datetime.time(10, 0), None],
                    index=pd.DatetimeIndex(['2002-02-03', '2010-01-11', '2010-01-13', '2011-01-10'])
                )
            )
        2002-02-03   2002-02-03 11:02:00+00:00
        2010-01-11   2010-01-12 11:01:00+00:00
        2010-01-13   2010-01-13 10:00:00+00:00
        2011-01-10                         NaT
        dtype: datetime64[ns, UTC]
        """
        col = (
            col.dropna()
        )  # Python 3.8, pandas 2.0.3 cannot create time deltas from NaT
        try:
            times = col.str[0]
        except AttributeError:  # no tuples, only offset 0
            return (
                (
                    pd.to_timedelta(col.astype("string").fillna(""), errors="coerce")
                    + col.index
                )
                .dt.tz_localize(self.tz)
                .dt.tz_convert("UTC")
            )

        return (
            (
                pd.to_timedelta(
                    times.fillna(col).astype("string").fillna(""), errors="coerce"
                )
                + pd.to_timedelta(col.str[1].fillna(0), unit="D")
                + col.index
            )
            .dt.tz_localize(self.tz)
            .dt.tz_convert("UTC")
        )

    @staticmethod
    def _col_name(n: int):
        return (
            f"interruption_start_{n // 2 + 1}"
            if n % 2 == 1
            else f"interruption_end_{n // 2}"
        )

    @property
    def interruptions_df(self):
        """
        Will return a pd.DataFrame only containing interruptions.
        """
        if not self.interruptions:
            return pd.DataFrame(index=pd.DatetimeIndex([]))
        intr = pd.DataFrame(self.interruptions)
        intr.index = pd.to_datetime(intr.pop(0))

        intr.columns = map(self._col_name, intr.columns)
        intr.index.name = None

        return intr.apply(self._convert).sort_index()

    def holidays(self) -> pd.tseries.offsets.CustomBusinessDay:
        """
        Returns the complete CustomBusinessDay object of holidays that can be used in any Pandas function that take
        that input.

        :return: CustomBusinessDay object of holidays
        """
        try:
            return self._holidays
        except AttributeError:
            self._holidays = CustomBusinessDay(
                holidays=self.adhoc_holidays,
                calendar=self.regular_holidays,
                weekmask=self.weekmask,
            )
        return self._holidays

    def valid_days(self, start_date, end_date, tz="UTC") -> pd.DatetimeIndex:
        """
        Get a DatetimeIndex of valid open business days.

        :param start_date: start date
        :param end_date: end date
        :param tz: time zone in either string or pytz.timezone
        :return: DatetimeIndex of valid business days
        """
        return pd.date_range(
            start_date, end_date, freq=self.holidays(), normalize=True, tz=tz
        )

    def _get_market_times(self, start, end):
        mts = self._market_times
        return mts[mts.index(start) : mts.index(end) + 1]

    def days_at_time(self, days, market_time, day_offset=0):
        """
        Create an index of days at time ``t``, interpreted in timezone ``tz``. The returned index is localized to UTC.

        In the example below, the times switch from 13:45 to 12:45 UTC because
        March 13th is the daylight savings transition for US/Eastern.  All the
        times are still 8:45 when interpreted in US/Eastern.

        >>> import pandas as pd; import datetime; import pprint
        >>> dts = pd.date_range('2016-03-12', '2016-03-14')
        >>> dts_at_845 = days_at_time(dts, datetime.time(8, 45), 'US/Eastern')
        >>> pprint.pprint([str(dt) for dt in dts_at_845])
        ['2016-03-12 13:45:00+00:00',
         '2016-03-13 12:45:00+00:00',
         '2016-03-14 12:45:00+00:00']

        :param days: DatetimeIndex An index of dates (represented as midnight).
        :param market_time: datetime.time The time to apply as an offset to each day in ``days``.
        :param day_offset: int The number of days we want to offset @days by
        :return: pd.Series of date with the time requested.
        """
        # Offset days without tz to avoid timezone issues.
        days = pd.DatetimeIndex(days).tz_localize(None).to_series()

        if isinstance(
            market_time, str
        ):  # if string, assume its a reference to saved market times
            timedeltas = self._regular_market_timedeltas[market_time]
            datetimes = days + timedeltas[0][1]
            for cut_off, timedelta in timedeltas[1:]:
                datetimes = datetimes.where(
                    days < pd.Timestamp(cut_off), days + timedelta
                )

        else:  # otherwise, assume it is a datetime.time object
            datetimes = days + self._tdelta(market_time, day_offset)

        return datetimes.dt.tz_localize(self.tz).dt.tz_convert("UTC")

    def _tryholidays(self, cal, s, e):
        try:
            # If the Calendar is all single Observance Holidays then it is far
            # more efficient to extract and return those dates
            observed_dates = u.all_single_observance_rules(cal)
            if observed_dates is not None:
                return pd.DatetimeIndex(
                    [date for date in observed_dates if s <= date <= e]
                )
            else:
                return cal.holidays(s, e)
        except ValueError:
            return pd.DatetimeIndex([])

    def _special_dates(self, calendars, ad_hoc_dates, start, end):
        """
        Union an iterable of pairs of the forms (time, calendar),
        (time, [dates]), and (time, int). If the second item in the pair
        is an int it will be interpreted as a specific day of the week.

        (This is shared logic for computing special opens and special closes.)
        """
        indexes = []
        for time_, calendar in calendars:
            if isinstance(calendar, int):
                day_of_week = CustomBusinessDay(weekmask=WEEKMASK_ABBR[calendar])
                indexes.append(
                    self.days_at_time(
                        pd.date_range(start, end, freq=day_of_week), time_
                    )
                )
            else:
                indexes.append(
                    self.days_at_time(self._tryholidays(calendar, start, end), time_)
                )

        indexes += [self.days_at_time(dates, time_) for time_, dates in ad_hoc_dates]

        if indexes:
            dates = pd.concat(indexes).sort_index().drop_duplicates()
            return dates.loc[start : end.replace(hour=23, minute=59, second=59)]

        return pd.Series([], dtype="datetime64[ns, UTC]", index=pd.DatetimeIndex([]))

    def special_dates(self, market_time, start_date, end_date, filter_holidays=True):
        """
        Calculate a datetimeindex that only contains the specail times of the requested market time.

        :param market_time: market_time reference
        :param start_date: first possible date of the index
        :param end_date: last possible date of the index
        :param filter_holidays: will filter days by self.valid_days, which can be useful when debugging

        :return: schedule DatetimeIndex
        """
        start_date, end_date = self.clean_dates(start_date, end_date)
        calendars = self.get_special_times(market_time)
        ad_hoc = self.get_special_times_adhoc(market_time)
        special = self._special_dates(calendars, ad_hoc, start_date, end_date)

        if filter_holidays:
            valid = self.valid_days(start_date, end_date, tz=None)
            special = special[
                special.index.isin(valid)
            ]  # some sources of special times don't exclude holidays
        return special

    def schedule(
        self,
        start_date,
        end_date,
        tz="UTC",
        start="market_open",
        end="market_close",
        force_special_times=True,
        market_times=None,
        interruptions=False,
    ) -> pd.DataFrame:
        """
        Generates the schedule DataFrame. The resulting DataFrame will have all the valid business days as the index
        and columns for the requested market times. The columns can be determined either by setting a range (inclusive
        on both sides), using `start` and `end`, or by passing a list to `market_times'. A range of market_times is
        derived from a list of market_times that are available to the instance, which are sorted based on the current
        regular time. See examples/usage.ipynb for demonstrations.

        All time zones are set to UTC by default. Setting the tz parameter will convert the columns to the desired
        timezone, such as 'America/New_York'.

        :param start_date: first date of the schedule
        :param end_date: last date of the schedule
        :param tz: timezone that the columns of the returned schedule are in, default: "UTC"
        :param start: the first market_time to include as a column, default: "market_open"
        :param end: the last market_time to include as a column, default: "market_close"
        :param force_special_times: how to handle special times.
            True: overwrite regular times of the column itself, conform other columns to special times of
                market_open/market_close if those are requested.
            False: only overwrite regular times of the column itself, leave others alone
            None: completely ignore special times
        :param market_times: alternative to start/end, list of market_times that are in self.regular_market_times
        :param interruptions: bool, whether to add interruptions to the schedule, default: False
            These will be added as columns to the right of the DataFrame. Any interruption on a day between
            start_date and end_date will be included, regardless of the market_times requested.
            Also, `force_special_times` does not take these into consideration.
        :return: schedule DataFrame
        """
        start_date, end_date = self.clean_dates(start_date, end_date)
        if not (start_date <= end_date):
            raise ValueError("start_date must be before or equal to end_date.")

        _all_days = self.valid_days(start_date, end_date)

        # Setup all valid trading days and the requested market_times
        if market_times is None:
            market_times = self._get_market_times(start, end)
        elif market_times == "all":
            market_times = self._market_times

        if not _all_days.size:  # If no valid days return an empty DataFrame
            return pd.DataFrame(
                columns=market_times, index=pd.DatetimeIndex([], freq="C")
            )

        return self.schedule_from_days(
            _all_days, tz, start, end, force_special_times, market_times, interruptions
        )

    def schedule_from_days(
        self,
        days: pd.DatetimeIndex,
        tz="UTC",
        start="market_open",
        end="market_close",
        force_special_times=True,
        market_times=None,
        interruptions=False,
    ) -> pd.DataFrame:
        """
        Generates a schedule DataFrame for the days provided. The days are assumed to be valid trading days.

        The columns can be determined either by setting a range (inclusive on both sides), using `start` and `end`,
        or by passing a list to `market_times'. A range of market_times is derived from a list of market_times that
        are available to the instance, which are sorted based on the current regular time.
        See examples/usage.ipynb for demonstrations.

        All time zones are set to UTC by default. Setting the tz parameter will convert the columns to the desired
        timezone, such as 'America/New_York'.

        :param days: pd.DatetimeIndex of all the desired days in ascending order. This function does not double check
            that these are valid trading days, it is assumed they are. It is intended that this parameter is generated
            by either the .valid_days() or .date_range_htf() methods. Time & Timezone Information is ignored.
        :param tz: timezone that the columns of the returned schedule are in, default: "UTC"
        :param start: the first market_time to include as a column, default: "market_open"
        :param end: the last market_time to include as a column, default: "market_close"
        :param force_special_times: how to handle special times.
            True: overwrite regular times of the column itself, conform other columns to special times of
                market_open/market_close if those are requested.
            False: only overwrite regular times of the column itself, leave others alone
            None: completely ignore special times
        :param market_times: alternative to start/end, list of market_times that are in self.regular_market_times
        :param interruptions: bool, whether to add interruptions to the schedule, default: False
            These will be added as columns to the right of the DataFrame. Any interruption on a day between
            start_date and end_date will be included, regardless of the market_times requested.
            Also, `force_special_times` does not take these into consideration.
        :return: schedule DataFrame
        """

        if days.dtype != "datetime64[ns]":
            days = pd.DatetimeIndex(days).normalize().tz_localize(None)

        # Setup all valid trading days and the requested market_times
        if market_times is None:
            market_times = self._get_market_times(start, end)
        elif market_times == "all":
            market_times = self._market_times

        _adj_others = force_special_times is True
        _adj_col = force_special_times is not None
        _open_adj = _close_adj = []

        schedule = pd.DataFrame()
        for market_time in market_times:
            temp = self.days_at_time(days, market_time).copy()  # standard times
            if _adj_col:
                # create an array of special times
                special = self.special_dates(
                    market_time, days[0], days[-1], filter_holidays=False
                )
                # overwrite standard times
                specialix = special.index[
                    special.index.isin(temp.index)
                ]  # some sources of special times don't exclude holidays
                temp.loc[specialix] = special

                if _adj_others:
                    if market_time == "market_open":
                        _open_adj = specialix
                    elif market_time == "market_close":
                        _close_adj = specialix

            schedule[market_time] = temp

        cols = schedule.columns
        if _adj_others and len(_open_adj) > 0:
            mkt_open_ind = cols.get_loc("market_open")

            # Can't use Lambdas here since numpy array assignment doesn't return the array.
            def adjust_opens(x):  # x is an np.Array.
                x[x <= x[mkt_open_ind]] = x[mkt_open_ind]
                return x

            adjusted = schedule.loc[_open_adj].apply(adjust_opens, axis=1, raw=True)
            schedule.loc[_open_adj] = adjusted

        if _adj_others and len(_close_adj) > 0:
            mkt_close_ind = cols.get_loc("market_close")

            def adjust_closes(x):
                x[x >= x[mkt_close_ind]] = x[mkt_close_ind]
                return x

            adjusted = schedule.loc[_close_adj].apply(adjust_closes, axis=1, raw=True)
            schedule.loc[_close_adj] = adjusted

        if interruptions:
            interrs = self.interruptions_df
            schedule[interrs.columns] = interrs
            schedule = schedule.dropna(how="all", axis=1)

        if tz != "UTC":
            schedule = schedule.apply(lambda s: s.dt.tz_convert(tz))

        return schedule

    def date_range_htf(
        self,
        frequency: Union[str, pd.Timedelta, int, float],
        start: Union[str, pd.Timestamp, int, float, None] = None,
        end: Union[str, pd.Timestamp, int, float, None] = None,
        periods: Union[int, None] = None,
        closed: Union[Literal["left", "right"], None] = "right",
        *,
        day_anchor: u.Day_Anchor = "SUN",
        month_anchor: u.Month_Anchor = "JAN",
    ) -> pd.DatetimeIndex:
        """
        Returns a Normalized DatetimeIndex from the start-date to End-Date for Time periods of 1D and Higher.

        PARAMETERS:

        :param frequency: String, Int/float (POSIX seconds) or pd.Timedelta of the desired frequency.
            :Must be Greater than '1D' and an integer multiple of the base frequency (D, W, M, Q, or Y)
            :Important Note: Ints/Floats & Timedeltas are always considered as 'Open Business Days',
                '2D' == Every Other Buisness Day, '3D' == Every 3rd B.Day, '7D' == Every 7th B.Day
            :Higher periods (passed as strings) align to the beginning or end of the relevant period
            :i.e. '1W' == First/[Last] Trading Day of each Week, '1Q' == First/[Last] Day of every Quarter

        :param start: String, Int/float (POSIX seconds) or pd.Timestamp of the desired start time.
            :The Time & Timezone information is ignored. Only the Normalized Day is considered.

        :param end: String, Int/float (POSIX seconds) or pd.Timestamp of the desired start time.
            :The Time & Timezone information is ignored. Only the Normalized Day is considered.

        :param periods: Optional Integer number of periods to return. If a Period count, Start time,
            and End time are given the period count is ignored.

        :param closed: Literal['left', 'right']. Method used to close each range.
            :Left: First open trading day of the Session is returned (e.g. First Open Day of The Month)
            :right: Last open trading day of the Session is returned (e.g. Last Open Day of The Month)
            :Note, This has no effect when the desired frequency is a number of days.

        :param day_anchor: Day to Anchor the start of the Weekly timeframes to. Default 'SUN'.
            : To get the First/Last Days of the trading Week then the Anchor needs to be on a day the relevant
                market is closed.
            : This can be set so that a specific day each week is returned.
            : freq='1W' & day_anchor='WED' Will return Every 'WED' when the market is open, and nearest day
                to the left or right (based on 'closed') when the market is closed.
            Options: ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]

        :param month_anchor: Month to Anchor the start of the year to for Quarter and yearly timeframes.
            : Default 'JAN' for Calendar Quarters/Years. Can be set to 'JUL' to return Fiscal Years
            Options: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
        """
        return u.date_range_htf(
            self.holidays(),
            frequency,
            start,
            end,
            periods,
            closed,
            day_anchor=day_anchor,
            month_anchor=month_anchor,
        )

    def open_at_time(self, schedule, timestamp, include_close=False, only_rth=False):
        """
        Determine if a given timestamp is during an open time for the market. If the timestamp is
        before the first open time or after the last close time of `schedule`, a ValueError will be raised.

        :param schedule: schedule DataFrame
        :param timestamp: the timestamp to check for. Assumed to be UTC, if it doesn't include tz information.
        :param include_close: if False then the timestamp that equals the closing timestamp will return False and not be
            considered a valid open date and time. If True then it will be considered valid and return True. Use True
            if using bars and would like to include the last bar as a valid open date and time. The close refers to the
            latest market_time available, which could be after market_close (e.g. 'post').
        :param only_rth: whether to ignore columns that are before market_open or after market_close. If true,
            include_close will be referring to market_close.
        :return: True if the timestamp is a valid open date and time, False if not
        """
        timestamp = pd.Timestamp(timestamp)
        try:
            timestamp = timestamp.tz_localize("UTC")
        except TypeError:
            pass

        cols = schedule.columns
        interrs = cols.str.startswith("interruption_")
        if not (cols.isin(self._oc_market_times) | interrs).all():
            raise ValueError(
                "You seem to be using a schedule that isn't based on the market_times, "
                "or includes market_times that are not represented in the open_close_map."
            )

        if only_rth:
            lowest, highest = "market_open", "market_close"
        else:
            cols = cols[~interrs]
            ix = cols.map(self._oc_market_times.index)
            lowest, highest = cols[ix == ix.min()][0], cols[ix == ix.max()][0]

        if timestamp < schedule[lowest].iat[0] or timestamp > schedule[highest].iat[-1]:
            raise ValueError("The provided timestamp is not covered by the schedule")

        day = schedule[schedule[lowest].le(timestamp)].iloc[-1].dropna().sort_values()
        day = day.loc[lowest:highest]
        day = day.index.to_series(index=day)

        if interrs.any():
            starts = day.str.startswith("interruption_start_")
            ends = day.str.startswith("interruption_end_")
            day.loc[starts] = False
            day.loc[ends] = True

        # When post follows market_close, market_close should not be considered a close
        day.loc[day.eq("market_close") & day.shift(-1).eq("post")] = "market_open"
        day = day.map(
            lambda x: (
                self.open_close_map.get(x) if x in self.open_close_map.keys() else x
            )
        )

        if include_close:
            below = day.index < timestamp
        else:
            below = day.index <= timestamp
        return bool(day[below].iat[-1])  # returns numpy.bool_ if not bool(...)

    # need this to make is_open_now testable
    @staticmethod
    def _get_current_time():
        return pd.Timestamp.now(tz="UTC")

    def is_open_now(self, schedule, include_close=False, only_rth=False):
        """
        To determine if the current local system time (converted to UTC) is an open time for the market

        :param schedule: schedule DataFrame
        :param include_close: if False then the function will return False if the current local system time is equal to
            the closing timestamp. If True then it will return True if the current local system time is equal to the
            closing timestamp. Use True if using bars and would like to include the last bar as a valid open date
            and time.
        :param only_rth: whether to consider columns that are before market_open or after market_close

        :return: True if the current local system time is a valid open date and time, False if not
        """
        current_time = MarketCalendar._get_current_time()
        return self.open_at_time(
            schedule, current_time, include_close=include_close, only_rth=only_rth
        )

    def clean_dates(self, start_date, end_date):
        """
        Strips the inputs of time and time zone information

        :param start_date: start date
        :param end_date: end date
        :return: (start_date, end_date) with just date, no time and no time zone
        """
        start_date = pd.Timestamp(start_date).tz_localize(None).normalize()
        end_date = pd.Timestamp(end_date).tz_localize(None).normalize()
        return start_date, end_date

    def is_different(self, col, diff=None):
        if diff is None:
            diff = pd.Series.ne
        normal = self.days_at_time(col.index, col.name)
        return diff(col.dt.tz_convert("UTC"), normal)

    def early_closes(self, schedule):
        """
        Get a DataFrame of the dates that are an early close.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are early closes
        """
        return schedule[self.is_different(schedule["market_close"], pd.Series.lt)]

    def late_opens(self, schedule):
        """
        Get a DataFrame of the dates that are an late opens.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are late opens
        """
        return schedule[self.is_different(schedule["market_open"], pd.Series.gt)]

    def __getitem__(self, item):
        if isinstance(item, (tuple, list)):
            if item[1] == "all":
                return self.get_time(item[0], all_times=True)
            else:
                return self.get_time_on(item[0], item[1])
        else:
            return self.get_time(item)

    def __setitem__(self, key, value):
        return self.add_time(key, value)

    def __delitem__(self, key):
        return self.remove_time(key)
