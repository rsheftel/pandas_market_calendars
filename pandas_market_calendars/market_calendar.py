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
    """
    There needs to be some kind of mapping of names of parts to their start and end times
    
    
    Stop worrying about parts ending in the middle of the day.
    
    make .schedule be able to take keywords that indicate which parts to start and which to end with 
       
    
    """

    # tz = None
    _all_market_times = {
        "market_open": {None: None},
        "market_close": {None: None}
    }
    def __init__(self, open_time=None, close_time=None):
        """
        :param open_time: Market open time override as datetime.time object. If None then default is used.
        :param close_time: Market close time override as datetime.time object. If None then default is used.
        """
        self._open_time = False if open_time is None else open_time
        self._close_time = False if close_time is None else close_time
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
    def open_time_default(self):
        """
        Default open time for the market

        :return: time
        """
        return self._all_market_times["market_open"][None]

    @property
    def close_time_default(self):
        """
        Default close time for the market

        :return: time
        """
        return self._all_market_times["market_close"][None]

    @property
    def break_start(self):
        """
        Break time start. If None then there is no break

        :return: time or None
        """
        try: return self._all_market_times["break_start"][None]
        except KeyError: return None


    @property
    def break_end(self):
        """
        Break time end. If None then there is no break

        :return: time or None
        """
        try: return self._all_market_times["break_end"][None]
        except KeyError: return None

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
        return getattr(self, "special_" + market_time)

    def get_special_times_adhoc(self, market_time):
        return getattr(self, "special_" + market_time + "_adhoc")

    @property
    def open_time(self):
        """

        :return: open time
        """
        return self._open_time or self.open_time_default

    @property
    def close_time(self):
        """

        :return: close time
        """
        return self._close_time or self.close_time_default

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

    def _get_market_times(self, start, end):
        start = self._sorted_market_times.index(start)  # _sorted_market_times is created by Meta
        end = self._sorted_market_times.index(end)
        return self._sorted_market_times[start: end+1]

    def _tdelta(self, t, day_offset= 0):
        return pd.Timedelta(days=day_offset, hours=t.hour, minutes=t.minute, seconds=t.second)

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
        :return: DatetimeIndex of date with the time t
        """

        # Offset days without tz to avoid timezone issues.
        days = DatetimeIndex(days).tz_localize(None)

        if isinstance(market_time, str):  # if string, assume its a reference to saved market times
            times = self._all_market_times[market_time]
            datetimes = days + self._tdelta(times[None])

            for cut_off in self._all_cut_offs[market_time]: # _all_cut_offs is set by Meta
                datetimes = datetimes.where(days >= pd.Timestamp(cut_off),
                                            days + times[cut_off])

        else: # otherwise, assume it is a datetime.time object
           datetimes = days + self._tdelta(market_time)

        return datetimes.tz_localize(self.tz).tz_convert('UTC')

    def schedule(self, start_date, end_date, tz='UTC',
                 start= "market_open", end= "market_close", ignore_special_times= False):
        """
        Generates the schedule DataFrame. The resulting DataFrame will have all the valid business days as the index
        and columns for the market opening datetime (market_open) and closing datetime (market_close). All time zones
        are set to UTC by default. Setting the tz parameter will convert the columns to the desired timezone,
        such as 'America/New_York'

        :param start_date: start date
        :param end_date: end date
        :param tz: timezone that the returned schedule is in
        :param start:
        :param end:
        :param ignore_special_times:
        :return: schedule DataFrame
        """
        start_date, end_date = self.clean_dates(start_date, end_date)
        if not (start_date <= end_date):
            raise ValueError('start_date must be before or equal to end_date.')

        # Setup all valid trading days and the requested market_times
        _all_days = self.valid_days(start_date, end_date)
        market_times = self._get_market_times(start, end)
        # If no valid days return an empty DataFrame
        if len(_all_days) == 0:
            return pd.DataFrame(columns=market_times, index=pd.DatetimeIndex([], freq='C'))

        columns = {}
        for market_time in market_times:
            temp = self.days_at_time(_all_days, market_time) # standard times

            if not ignore_special_times:
                # create an array of special times
                calendars = self.get_special_times(market_time)
                ad_hoc = self.get_special_times_adhoc(market_time)
                special = self._special_dates(calendars, ad_hoc, start_date, end_date)

                # overwrite standard times
                temp = temp.to_series(index= _all_days)
                temp.loc[special.normalize()] = special

            columns[market_time] = temp

        schedule = pd.DataFrame(columns, index= _all_days.tz_localize(None), columns= market_times)

        # now adjust any quirks that come through odd times
        """
        What is the problem?
        
        there may be time
        
        
        
        
        """



        return schedule

    def _tryholidays(self, cal, s, e):
        try: return cal.holidays(s, e)
        except ValueError: return pd.DatetimeIndex([])

    def _special_dates(self, calendars, ad_hoc_dates, start_date, end_date):
        """
        Union an iterable of pairs of the form (time, calendar)
        and an iterable of pairs of the form (time, [dates])

        (This is shared logic for computing special opens and special closes.)
        """
        s = start_date.tz_localize("UTC")
        e = end_date.tz_localize("UTC")
        dates = pd.DatetimeIndex([], tz= "UTC").union_many(
            [
                self.days_at_time(
                    self._tryholidays(calendar, s.tz_localize(None), e.tz_localize(None)), time_)
                      for time_, calendar in calendars
             ] + [
                self.days_at_time(dates, time_)
                  for time_, dates in ad_hoc_dates
            ])

        return dates[dates.ge(s) & dates.le(e.replace(hour=23, minute=59, second=59))]


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
        date = pd.Timestamp(timestamp).tz_convert('UTC').normalize()
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

    def early_closes(self, schedule):
        """
        Get a DataFrame of the dates that are an early close.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are early closes
        """
        match_dates = schedule['market_close'].apply(lambda x: x.tz_convert(self.tz).time() != self.close_time)
        return schedule[match_dates]

    def late_opens(self, schedule):
        """
        Get a DataFrame of the dates that are an late opens.

        :param schedule: schedule DataFrame
        :return: schedule DataFrame with rows that are late opens
        """
        match_dates = schedule['market_open'].apply(lambda x: x.tz_convert(self.tz).time() != self.open_time)
        return schedule[match_dates]