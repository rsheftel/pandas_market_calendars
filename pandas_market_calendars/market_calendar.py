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

from abc import ABCMeta, abstractmethod
from itertools import compress

import pandas as pd
from pandas import DataFrame, DatetimeIndex
from pandas.tseries.offsets import CustomBusinessDay

from .class_registry import RegisteryMeta

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


class MarketCalendarMeta(ABCMeta, RegisteryMeta):
    pass


class MarketCalendar(metaclass=MarketCalendarMeta):
    """
    An MarketCalendar represents the timing information of a single market or exchange.
    Unless otherwise noted all times are in UTC and use Pandas data structures.
    """

    def __init__(self, open_time=None, close_time=None):
        """
        :param open_time: Market open time override as datetime.time object. If None then default is used.
        :param close_time: Market close time override as datetime.time object. If None then default is used.
        """
        self._open_time = self.open_time_default if open_time is None else open_time
        self._close_time = self.close_time_default if close_time is None else close_time
        self._holidays = None

    @classmethod
    def factory(cls, name, open_time=None, close_time=None):
        """
        :param name: The name of the MarketCalendar to be retrieved.
        :param open_time: Market open time override as datetime.time object. If None then default is used.
        :param close_time: Market close time override as datetime.time object. If None then default is used.
        :return: MarketCalendar of the desired calendar.
        """
        return cls._regmeta_instance_factory(name, open_time=open_time, close_time=close_time)

    @classmethod
    def calendar_names(cls):
        """All Market Calendar names and aliases that can be used in "factory"
        :return: list(str)
        """
        return [cal for cal in cls._regmeta_classes() if cal not in ['MarketCalendar', 'TradingCalendar']]

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
    def tz(self):
        """
        Time zone for the market.

        :return: timezone
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def open_time_default(self):
        """
        Default open time for the market

        :return: time
        """
        raise NotImplementedError()

    @property
    @abstractmethod
    def close_time_default(self):
        """
        Default close time for the market

        :return: time
        """
        raise NotImplementedError()

    @property
    def break_start(self):
        """
        Break time start. If None then there is no break

        :return: time or None
        """
        return None

    @property
    def break_end(self):
        """
        Break time end. If None then there is no break

        :return: time or None
        """
        return None

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

    @property
    def open_time(self):
        """

        :return: open time
        """
        return self._open_time

    @property
    def close_time(self):
        """

        :return: close time
        """
        return self._close_time

    @property
    def open_offset(self):
        """

        :return: open offset
        """
        return 0

    @property
    def close_offset(self):
        """

        :return: close offset
        """
        return 0

    def holidays(self):
        """
        Returns the complete CustomBusinessDay object of holidays that can be used in any Pandas function that take
        that input.

        :return: CustomBusinessDay object of holidays
        """
        if self._holidays is None:
            self._holidays = CustomBusinessDay(
                holidays=self.adhoc_holidays,
                calendar=self.regular_holidays,
                weekmask=self.weekmask,
            )
        return self._holidays

    def valid_days(self, start_date, end_date, tz='UTC'):
        """
        Get a DatetimeIndex of valid open business days.

        :param start_date: start date
        :param end_date: end date
        :param tz: time zone in either string or pytz.timezone
        :return: DatetimeIndex of valid business days
        """
        return pd.date_range(start_date, end_date, freq=self.holidays(), normalize=True, tz=tz)

    def schedule(self, start_date, end_date, tz='UTC'):
        """
        Generates the schedule DataFrame. The resulting DataFrame will have all the valid business days as the index
        and columns for the market opening datetime (market_open) and closing datetime (market_close). All time zones
        are set to UTC by default. Setting the tz parameter will convert the columns to the desired timezone,
        such as 'America/New_York'

        :param start_date: start date
        :param end_date: end date
        :param tz: timezone
        :return: schedule DataFrame
        """
        start_date, end_date = clean_dates(start_date, end_date)
        if not (start_date <= end_date):
            raise ValueError('start_date must be before or equal to end_date.')

        # Setup all valid trading days
        _all_days = self.valid_days(start_date, end_date)

        # If no valid days return an empty DataFrame
        if len(_all_days) == 0:
            return pd.DataFrame(columns=['market_open', 'market_close'], index=pd.DatetimeIndex([], freq='C'))

        # `DatetimeIndex`s of standard opens/closes for each day.
        opens = days_at_time(_all_days, self.open_time, self.tz, self.open_offset).tz_convert(tz)
        closes = days_at_time(_all_days, self.close_time, self.tz, self.close_offset).tz_convert(tz)

        # `DatetimeIndex`s of nonstandard opens/closes
        _special_opens = self._calculate_special_opens(start_date, end_date)
        _special_closes = self._calculate_special_closes(start_date, end_date)

        # Overwrite the special opens and closes on top of the standard ones.
        _overwrite_special_dates(_all_days, opens, _special_opens)
        _overwrite_special_dates(_all_days, closes, _special_closes)

        result = DataFrame(index=_all_days.tz_localize(None), columns=['market_open', 'market_close'],
                           data={'market_open': opens, 'market_close': closes})

        if self.break_start:
            result['break_start'] = days_at_time(_all_days, self.break_start, self.tz).tz_convert(tz)
            temp = result[['market_open', 'break_start']].max(axis=1)
            result['break_start'] = temp
            result['break_end'] = days_at_time(_all_days, self.break_end, self.tz).tz_convert(tz)
            temp = result[['market_close', 'break_end']].min(axis=1)
            result['break_end'] = temp

        return result

    @staticmethod
    def open_at_time(schedule, timestamp, include_close=False):
        """
        To determine if a given timestamp is during an open time for the market.

        :param schedule: schedule DataFrame
        :param timestamp: the timestamp to check for
        :param include_close: if False then the timestamp that equals the closing timestamp will return False and not be
            considered a valid open date and time. If True then it will be considered valid and return True. Use True
            if using bars and would like to include the last bar as a valid open date and time.
        :return: True if the timestamp is a valid open date and time, False if not
        """
        date = pd.Timestamp(pd.Timestamp(timestamp).tz_convert('UTC').date())
        if date in schedule.index:
            if 'break_start' in schedule.columns:
                if include_close:
                    return (schedule.at[date, 'market_open'] <= timestamp <= schedule.at[date, 'break_start']) or \
                           (schedule.at[date, 'break_end'] <= timestamp <= schedule.at[date, 'market_close'])
                else:
                    return (schedule.at[date, 'market_open'] <= timestamp < schedule.at[date, 'break_start']) or \
                           (schedule.at[date, 'break_end'] <= timestamp < schedule.at[date, 'market_close'])
            else:
                if include_close:
                    return schedule.at[date, 'market_open'] <= timestamp <= schedule.at[date, 'market_close']
                else:
                    return schedule.at[date, 'market_open'] <= timestamp < schedule.at[date, 'market_close']
        else:
            return False

    # need this to make is_open_now testable
    @staticmethod
    def _get_current_time():
        return pd.Timestamp.now(tz='UTC')

    @staticmethod
    def is_open_now(schedule, include_close=False):
        """
        To determine if the current local system time (converted to UTC) is an open time for the market

        :param schedule: schedule DataFrame
        :param include_close: if False then the function will return False if the current local system time is equal to
            the closing timestamp. If True then it will return True if the current local system time is equal to the
            closing timestamp. Use True if using bars and would like to include the last bar as a valid open date
            and time.
        :return: True if the current local system time is a valid open date and time, False if not
        """
        current_time = MarketCalendar._get_current_time()
        return MarketCalendar.open_at_time(schedule, current_time)

    def early_closes(self, schedule):
        """
        Get a DataFrame of the dates that are an early close.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are early closes
        """
        match_dates = schedule['market_close'].apply(lambda x: x.tz_convert(self.tz).time() != self.close_time)
        return schedule[match_dates]

    def _special_dates(self, calendars, ad_hoc_dates, start_date, end_date):
        """
        Union an iterable of pairs of the form (time, calendar)
        and an iterable of pairs of the form (time, [dates])

        (This is shared logic for computing special opens and special closes.)
        """
        _dates = DatetimeIndex([], tz='UTC').union_many(
            [
                holidays_at_time(calendar, start_date, end_date, time_,
                                 self.tz)
                for time_, calendar in calendars
            ] + [
                days_at_time(datetimes, time_, self.tz)
                for time_, datetimes in ad_hoc_dates
            ]
        )
        # make the start_date and end_dates UTC and covert the entire day
        start_date = start_date.tz_localize('UTC')
        end_date = end_date.tz_localize('UTC').replace(hour=23, minute=59, second=59)
        return _dates[(_dates >= start_date) & (_dates <= end_date)]

    def _calculate_special_opens(self, start, end):
        return self._special_dates(
            self.special_opens,
            self.special_opens_adhoc,
            start,
            end,
        )

    def _calculate_special_closes(self, start, end):
        return self._special_dates(
            self.special_closes,
            self.special_closes_adhoc,
            start,
            end,
        )


def days_at_time(days, t, tz, day_offset=0):
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
    :param t: datetime.time The time to apply as an offset to each day in ``days``.
    :param tz: pytz.timezone The timezone to use to interpret ``t``.
    :param day_offset: int The number of days we want to offset @days by
    :return: DatetimeIndex of date with the time t
    """
    if len(days) == 0:
        return pd.DatetimeIndex(days).tz_localize(tz).tz_convert('UTC')

    # Offset days without tz to avoid timezone issues.
    days = DatetimeIndex(days).tz_localize(None)
    delta = pd.Timedelta(
        days=day_offset,
        hours=t.hour,
        minutes=t.minute,
        seconds=t.second,
    )
    return (days + delta).tz_localize(tz).tz_convert('UTC')


def holidays_at_time(calendar, start, end, time, tz):
    # Not sure why this fails, but this should trap it until resolved
    try:
        holidays = calendar.holidays(
            # Workaround for https://github.com/pydata/pandas/issues/9825.
            start.tz_localize(None),
            end.tz_localize(None),
        )
    except ValueError:
        holidays = pd.DatetimeIndex([])

    return days_at_time(
        holidays,
        time,
        tz=tz,
    )


def _overwrite_special_dates(midnight_utcs,
                             opens_or_closes,
                             special_opens_or_closes):
    """
    Overwrite dates in open_or_closes with corresponding dates in
    special_opens_or_closes, using midnight_utcs for alignment.
    """
    # Short circuit when nothing to apply.
    if not len(special_opens_or_closes):
        return

    len_m, len_oc = len(midnight_utcs), len(opens_or_closes)
    if len_m != len_oc:
        raise ValueError(
            "Found misaligned dates while building calendar.\n"
            "Expected midnight_utcs to be the same length as open_or_closes,\n"
            "but len(midnight_utcs)=%d, len(open_or_closes)=%d" % (len_m, len_oc)
        )

    # Find the array indices corresponding to each special date.
    indexer = midnight_utcs.get_indexer(special_opens_or_closes.normalize())

    # -1 indicates that no corresponding entry was found.  If any -1s are
    # present, then we have special dates that doesn't correspond to any
    # trading day. Filter these out
    good_indexes = [i != -1 for i in indexer]
    indexer = list(compress(indexer, good_indexes))

    # NOTE: This is a slightly dirty hack.  We're in-place overwriting the
    # internal data of an Index, which is conceptually immutable.  Since we're
    # maintaining sorting, this should be ok, but this is a good place to
    # sanity check if things start going haywire with calendar computations.
    opens_or_closes.values[indexer] = special_opens_or_closes.values[good_indexes]


def clean_dates(start_date, end_date):
    """
    Strips the inputs of time and time zone information

    :param start_date: start date
    :param end_date: end date
    :return: (start_date, end_date) with just date, no time and no time zone
    """
    start_date = pd.Timestamp(start_date).tz_localize(None).normalize()
    end_date = pd.Timestamp(end_date).tz_localize(None).normalize()
    return start_date, end_date
