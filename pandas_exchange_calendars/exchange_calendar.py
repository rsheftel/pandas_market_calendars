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

from abc import ABCMeta, abstractproperty
import datetime

import pandas as pd
from pandas import DataFrame, DatetimeIndex
from pandas.tseries.offsets import CustomBusinessDay

MONDAY, TUESDAY, WEDNESDAY, THURSDAY, FRIDAY, SATURDAY, SUNDAY = range(7)


class ExchangeCalendar(metaclass=ABCMeta):
    """
    An ExchangeCalendar represents the timing information of a single market
    exchange.

    The timing information is made up of two parts: sessions, and opens/closes.

    A session represents a contiguous set of minutes, and has a label that is
    midnight UTC. It is important to note that a session label should not be
    considered a specific point in time, and that midnight UTC is just being
    used for convenience.

    For each session, we store the open and close time in UTC time.
    """

    open_time_default = None
    close_time_default = None

    def __init__(self, open_time=None, close_time=None):
        self._open_time = self.open_time_default if open_time is None else open_time
        self._close_time = self.close_time_default if close_time is None else close_time

    @abstractproperty
    def name(self):
        raise NotImplementedError()

    @abstractproperty
    def tz(self):
        raise NotImplementedError()

    @property
    def regular_holidays(self):
        """
        Returns
        -------
        pd.AbstractHolidayCalendar: a calendar containing the regular holidays
        for this calendar
        """
        return None

    @property
    def adhoc_holidays(self):
        return []

    @property
    def special_opens(self):
        """
        A list of special open times and corresponding HolidayCalendars.

        Returns
        -------
        list: List of (time, AbstractHolidayCalendar) tuples
        """
        return []

    @property
    def special_opens_adhoc(self):
        """
        Returns
        -------
        list: List of (time, DatetimeIndex) tuples that represent special
         closes that cannot be codified into rules.
        """
        return []

    @property
    def special_closes(self):
        """
        A list of special close times and corresponding HolidayCalendars.

        Returns
        -------
        list: List of (time, AbstractHolidayCalendar) tuples
        """
        return []

    @property
    def special_closes_adhoc(self):
        """
        Returns
        -------
        list: List of (time, DatetimeIndex) tuples that represent special
         closes that cannot be codified into rules.
        """
        return []

    # -----

    @property
    def open_time(self):
        return self._open_time

    @property
    def close_time(self):
        return self._close_time

    @property
    def open_offset(self):
        return 0

    @property
    def close_offset(self):
        return 0

    def holidays(self):
        return CustomBusinessDay(
            holidays=self.adhoc_holidays,
            calendar=self.regular_holidays,
        )

    def valid_days(self, start_date, end_date, tz='UTC'):
        return pd.date_range(start_date, end_date, freq=self.holidays(), normalize=True, tz=tz)

    def schedule(self, start_date, end_date):
        start_date, end_date = clean_dates(start_date, end_date)

        # Setup all valid trading days
        _all_days = self.valid_days(start_date, end_date)

        # `DatetimeIndex`s of standard opens/closes for each day.
        opens = days_at_time(_all_days, self.open_time, self.tz, self.open_offset)
        closes = days_at_time(_all_days, self.close_time, self.tz, self.close_offset)

        # `DatetimeIndex`s of nonstandard opens/closes
        _special_opens = self._calculate_special_opens(start_date, end_date)
        _special_closes = self._calculate_special_closes(start_date, end_date)

        # Overwrite the special opens and closes on top of the standard ones.
        _overwrite_special_dates(_all_days, opens, _special_opens)
        _overwrite_special_dates(_all_days, closes, _special_closes)

        return DataFrame(index=_all_days.tz_localize(None), columns=['market_open', 'market_close'],
                         data={'market_open': opens, 'market_close': closes})

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
    Create an index of days at time ``t``, interpreted in timezone ``tz``.

    The returned index is localized to UTC.

    Parameters
    ----------
    days : DatetimeIndex
        An index of dates (represented as midnight).
    t : datetime.time
        The time to apply as an offset to each day in ``days``.
    tz : pytz.timezone
        The timezone to use to interpret ``t``.
    day_offset : int
        The number of days we want to offset @days by

    Example
    -------
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
    """
    if len(days) == 0:
        return days.tz_localize(tz).tz_convert('UTC')

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
    return days_at_time(
        calendar.holidays(
            # Workaround for https://github.com/pydata/pandas/issues/9825.
            start.tz_localize(None),
            end.tz_localize(None),
        ),
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
            "but len(midnight_utcs)=%d, len(open_or_closes)=%d" % len_m, len_oc
        )

    # Find the array indices corresponding to each special date.
    indexer = midnight_utcs.get_indexer(special_opens_or_closes.normalize())

    # -1 indicates that no corresponding entry was found.  If any -1s are
    # present, then we have special dates that doesn't correspond to any
    # trading day.
    if -1 in indexer:
        bad_dates = list(special_opens_or_closes[indexer == -1])
        raise ValueError("Special dates %s are not trading days." % bad_dates)

    # NOTE: This is a slightly dirty hack.  We're in-place overwriting the
    # internal data of an Index, which is conceptually immutable.  Since we're
    # maintaining sorting, this should be ok, but this is a good place to
    # sanity check if things start going haywire with calendar computations.
    opens_or_closes.values[indexer] = special_opens_or_closes.values


def clean_dates(start_date, end_date):
    start_date = pd.Timestamp(start_date).tz_localize(None).normalize()
    end_date = pd.Timestamp(end_date).tz_localize(None).normalize()
    return start_date, end_date
