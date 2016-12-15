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

from datetime import time
import pandas as pd
from pytz import timezone
from toolz import concat
from pandas.util.testing import assert_series_equal
from itertools import chain

from pandas_exchange_calendars import get_calendar
from pandas_exchange_calendars.calendar_utils import _calendars, _aliases
from pandas_exchange_calendars.exchange_calendar import days_at_time, ExchangeCalendar, is_sub_daily, clean_dates

from pandas.tseries.holiday import AbstractHolidayCalendar
from pandas_exchange_calendars.us_holidays import (
    USNewYearsDay,
    Christmas,
    HurricaneSandyClosings,
    USNationalDaysofMourning,
    MonTuesThursBeforeIndependenceDay
)


class FakeCalendar(ExchangeCalendar):
    open_time_default = time(11, 13)
    close_time_default = time(11, 49)

    @property
    def name(self):
        return "DMY"

    @property
    def tz(self):
        return "Asia/Ulaanbaatar"

    @property
    def regular_holidays(self):
        return AbstractHolidayCalendar(rules=[USNewYearsDay, Christmas])

    @property
    def adhoc_holidays(self):
        return list(chain(HurricaneSandyClosings, USNationalDaysofMourning))

    @property
    def special_opens(self):
        return [(time(11, 15), AbstractHolidayCalendar(rules=[MonTuesThursBeforeIndependenceDay]))]

    @property
    def special_opens_adhoc(self):
        return [(time(11, 20), ['2016-12-13'])]

    @property
    def special_closes(self):
        return [(time(11, 30), AbstractHolidayCalendar(rules=[MonTuesThursBeforeIndependenceDay]))]

    @property
    def special_closes_adhoc(self):
        return [(time(11, 40), ['2016-12-14'])]


def test_default_calendars():
    for name in concat([_calendars, _aliases]):
        assert get_calendar(name) is not None


def test_days_at_time():
    def dat(day, day_offset, time_offset, tz, expected):
        days = pd.DatetimeIndex([pd.Timestamp(day, tz=tz)])
        result = days_at_time(days, time_offset, tz, day_offset)[0]
        expected = pd.Timestamp(expected, tz=tz).tz_convert('UTC')
        assert result == expected

    args_list = [
        # NYSE standard day
        (
            '2016-07-19', 0, time(9, 31), timezone('America/New_York'),
            '2016-07-19 9:31',
        ),
        # CME standard day
        (
            '2016-07-19', -1, time(17, 1), timezone('America/Chicago'),
            '2016-07-18 17:01',
        ),
        # CME day after DST start
        (
            '2004-04-05', -1, time(17, 1), timezone('America/Chicago'),
            '2004-04-04 17:01'
        ),
        # ICE day after DST start
        (
            '1990-04-02', -1, time(19, 1), timezone('America/Chicago'),
            '1990-04-01 19:01',
        ),
    ]

    for args in args_list:
        dat(args[0], args[1], args[2], args[3], args[4])


def test_is_sub_daily():
    assert is_sub_daily('1min') is True
    assert is_sub_daily('5min') is True
    assert is_sub_daily('min') is True
    assert is_sub_daily('1H') is True
    assert is_sub_daily('H') is True

    assert is_sub_daily('D') is False
    assert is_sub_daily('1D') is False


def test_clean_dates():
    start, end = clean_dates('2016-12-01', '2016-12-31')
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = clean_dates('2016-12-01 12:00', '2016-12-31 12:00')
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = clean_dates(pd.Timestamp('2016-12-01', tz='America/Chicago'),
                             pd.Timestamp('2016-12-31', tz='America/New_York'))
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')

    start, end = clean_dates(pd.Timestamp('2016-12-01 09:31', tz='America/Chicago'),
                             pd.Timestamp('2016-12-31 16:00', tz='America/New_York'))
    assert start == pd.Timestamp('2016-12-01')
    assert end == pd.Timestamp('2016-12-31')


def test_schedule():
    cal = FakeCalendar()

    results = cal.schedule('2016-12-01', '2016-12-31')
    assert len(results) == 21

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 03:13:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-01 03:49:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-01 00:00:00+0000', tz='UTC', freq='C'),
                         index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[0], expected)

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 03:13:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-30 03:49:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-30 00:00:00+0000', tz='UTC', freq='C'),
                         index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[-1], expected)


def test_schedule_w_times():
    cal = FakeCalendar(time(12, 12), time(13, 13))

    results = cal.schedule('2016-12-01', '2016-12-31')
    assert len(results) == 21

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-01 04:12:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-01 05:13:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-01 00:00:00+0000', tz='UTC', freq='C'),
                         index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[0], expected)

    expected = pd.Series({'market_open': pd.Timestamp('2016-12-30 04:12:00+0000', tz='UTC', freq='B'),
                          'market_close': pd.Timestamp('2016-12-30 05:13:00+0000', tz='UTC', freq='B')},
                         name=pd.Timestamp('2016-12-30 00:00:00+0000', tz='UTC', freq='C'),
                         index=['market_open', 'market_close'], dtype=object)
    assert_series_equal(results.iloc[-1], expected)


def test_date_range():
    cal = FakeCalendar()

    # no holidays

    # closed days

    # early close

    # late open
